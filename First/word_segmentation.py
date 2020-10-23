import copy

msr_training_utf8 = open('msr_training.utf8.ic', 'r', encoding='utf-8')
msr_str = msr_training_utf8.read()
msr_training_utf8.close()
msr_list = msr_str.split('\n')

head_dict = {
    'B':0,
    'M':1,
    'E':2,
    'S':3,
}
reverse_head_dict ={
    0:'B',
    1:'M',
    2:'E',
    3:'S',
}

msr_pro_dict_txt = open('msr_pro_dict.txt', 'r', encoding='utf-8')
msr_pro_dict = eval(msr_pro_dict_txt.read())
msr_pro_dict_txt.close()

last_word_pro_dict_txt = open('last_word_pro_dict.txt', 'r', encoding='utf-8')
last_word_pro_dict = eval(last_word_pro_dict_txt.read())
last_word_pro_dict_txt.close()

next_word_pro_dict_txt = open('next_word_pro_dict.txt', 'r', encoding='utf-8')
next_word_pro_dict = eval(next_word_pro_dict_txt.read())
next_word_pro_dict_txt.close()

msr_double_array_pro_dict_txt = open('msr_double_array_pro_dict.txt', 'r', encoding='utf-8')
msr_double_array_pro_dict = eval(msr_double_array_pro_dict_txt.read())
msr_double_array_pro_dict_txt.close()

str_test = input('输入一句话：')
segmentation_list = []
path_list = []

for i in str_test:
    segmentation_list.append([i, 0, 0, 0, 0])

path_list = copy.deepcopy(segmentation_list)

for i in range(len(segmentation_list)):
    if i == 0:
        # 代表第一个字，首字需要注意没有上一个字，只需要计算W后和R
        W_before = 0
        R = 0
        for j in range(4):
            string_last_word = segmentation_list[i][0]  # 希
            string_current_word = segmentation_list[i+1][0]  # 腊
            if string_last_word+reverse_head_dict[j]+string_current_word in next_word_pro_dict:
                W_before = next_word_pro_dict[string_last_word+reverse_head_dict[j]+string_current_word]
            if string_last_word in msr_pro_dict:
                R = msr_pro_dict[string_last_word][j]
            segmentation_list[i][j + 1] = W_before + R
        continue

    if i < len(segmentation_list) - 1:
        # 中间的所有字都有上下
        string_last_word = segmentation_list[i - 1][0]
        string_current_word = segmentation_list[i][0]
        string_next_word = segmentation_list[i + 1][0]

        for a in range(4):  # 遍历当前文字的四种状态
            last_word_pro = 0
            next_word_pro = 0
            R = 0
            P = 0
            # 判断上面一个字的哪个状态导致的这个字的某个状态

            max_index = 0
            for b in range(1, 4):  # 求上一个字的四种状态对应的式子最大值和他的index
                if string_last_word in msr_double_array_pro_dict:
                    if msr_double_array_pro_dict[string_last_word][max_index][a] * segmentation_list[i-1][max_index+1] < \
                            msr_double_array_pro_dict[string_last_word][b][a] * segmentation_list[i-1][b+1]:
                        max_index = b

            if string_last_word+string_current_word+reverse_head_dict[a] in last_word_pro_dict:
                last_word_pro = last_word_pro_dict[string_last_word+string_current_word+reverse_head_dict[a]]
            if string_current_word+reverse_head_dict[a]+string_next_word in next_word_pro_dict:
                next_word_pro = next_word_pro_dict[string_current_word+reverse_head_dict[a]+string_next_word]
            if string_current_word in msr_pro_dict:
                R = msr_pro_dict[string_current_word][a]
            if string_last_word in msr_double_array_pro_dict:
                P = msr_double_array_pro_dict[string_last_word][max_index][a]
            segmentation_list[i][a+1] = P * segmentation_list[i-1][max_index + 1] + \
                                      last_word_pro + next_word_pro + R
            path_list[i][a+1] = max_index

    if i == len(segmentation_list) - 1:
        string_last_word = segmentation_list[len(segmentation_list) - 2][0]
        string_current_word = segmentation_list[len(segmentation_list) - 1][0]
        for a in range(4):
            last_word_pro = 0
            P = 0
            R = 0
            max_index = 0
            for b in range(1, 4):  # 求上一个字的四种状态对应的式子最大值和他的index
                if string_current_word in msr_double_array_pro_dict:
                    if msr_double_array_pro_dict[string_current_word][max_index][a] * segmentation_list[i - 1][max_index + 1] < \
                            msr_double_array_pro_dict[string_current_word][b][a] * segmentation_list[i - 1][b + 1]:
                        max_index = b
            if string_last_word+string_current_word+reverse_head_dict[a] in last_word_pro_dict:
                last_word_pro = last_word_pro_dict[string_last_word+string_current_word+reverse_head_dict[a]]
            if string_current_word in msr_double_array_pro_dict:
                P = msr_double_array_pro_dict[string_current_word][max_index][a]
            if string_current_word in msr_pro_dict:
                R = last_word_pro + msr_pro_dict[string_current_word][a]
            segmentation_list[len(segmentation_list) - 1][a+1] = \
                P * segmentation_list[i - 1][max_index + 1] + R
            path_list[len(segmentation_list) - 1][a+1] = max_index

# for i in segmentation_list:
#     print(i)
# for i in path_list:
#     print(i)

max_index = 0
for i in range(1, 4):
    if segmentation_list[-1][i+1] > segmentation_list[-1][max_index+1]:
        max_index = i
str_sentence = ''
index = max_index
str_sentence = segmentation_list[-1][0] + reverse_head_dict[max_index] + str_sentence
for i in range(0, len(segmentation_list)-1):
    index = path_list[-1-i][index + 1]
    str_sentence = segmentation_list[-2-i][0] + reverse_head_dict[index] + str_sentence

for i in segmentation_list:
    print(i)
for i in path_list:
    print(i)
print(str_sentence)

string_sentence = ''
for s in str_sentence:
    if s == 'E' or s == 'S':
        string_sentence += ' '
    elif s == 'B' or s == 'M':
        continue
    else:
        string_sentence += s
print('分词结果：' + string_sentence)