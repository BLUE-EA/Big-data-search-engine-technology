# _*_ coding:utf-8 _*_

import copy

str_test = input('输入一句话：')
print('正在进行特征学习...')

msr_training_utf8 = open('msr_training.utf8.ic', 'r', encoding='utf-8-sig')
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

# 特征学习第一步计算字符出现次数
print('第一步特征学习')
count_dict = {}
for x in msr_list:
    if len(x) != 0:
        if x[0] in count_dict:
            pass
        else:
            count_dict[x[0]] = 0
        count_dict[x[0]] = count_dict[x[0]] + 1
    else:
        msr_list.remove(x)


# 特征学习第二步：
print('第二步特征学习')
msr_number_dict = {}
msr_pro_dict = {}

for x in msr_list:
    if x[2] == '|':
        continue
    if x[0] in msr_number_dict:
        pass
    else:
        msr_number_dict[x[0]] = [0, 0, 0, 0]
    current_index = head_dict[x[2]]
    msr_number_dict[x[0]][current_index] += 1
msr_pro_dict = copy.deepcopy(msr_number_dict)

for word in msr_number_dict:
    for i in range(4):
        msr_pro_dict[word][i] = msr_number_dict[word][i] / count_dict[word]


# 第三步特征计算：计算一个字的状态变化概率
print('第三步特征学习')
msr_double_array_dict = {}
msr_double_array_pro_dict = {}
last_word = ''
last_status = 'K'
count1 = 0
for i in msr_list:
    if i[2] == '|':
        continue
    if i[0] in msr_double_array_dict:
        pass
    else:
        msr_double_array_dict[i[0]] = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
    if last_word == '' and last_status == 'K':
        last_word = i[0]
        last_status = i[2]
        continue
    else:
        current_word = i[0]
        current_status = i[2]
        last_status_index = head_dict[last_status]
        next_status_index = head_dict[current_status]
        msr_double_array_dict[last_word][last_status_index][next_status_index] += 1
        last_word = current_word
        last_status = current_status
    count1 = count1+1
    # if count1 % 10000 == 0:
    #     print(count1)

msr_double_array_pro_dict = copy.deepcopy(msr_double_array_dict)

for word in msr_double_array_pro_dict:
    for a in range(4):
        for b in range(4):
            if msr_number_dict[word][a] == 0:
                continue
            msr_double_array_pro_dict[word][a][b] = msr_double_array_pro_dict[word][a][b] / msr_number_dict[word][a]


# 第四步特征计算
print('第四步特征学习')
last_word_dict = {}
next_word_dict = {}
last_word = ''
last_status = 'K'
current_word = ''
current_status = 'K'
for i in msr_list:
    if i[2] == '|':
        continue

    if last_word == '' and last_status == 'K':
        last_word = i[0]
        last_status = i[2]
        continue

    elif current_word == '' and current_status == 'K':
        current_word = i[0]
        current_status = i[2]
        continue
    else:
        next_word = i[0]
        next_status = i[2]

        if last_word+current_word+current_status in last_word_dict:
            last_word_dict[last_word+current_word+current_status] += 1
        else:
            last_word_dict[last_word+current_word+current_status] = 1

        if current_word+current_status+next_word in next_word_dict:
            next_word_dict[current_word+current_status+next_word] += 1
        else:
            next_word_dict[current_word+current_status+next_word] = 1

        last_word = copy.deepcopy(current_word)
        last_status = copy.deepcopy(current_status)

        current_word = copy.deepcopy(next_word)
        current_status = copy.deepcopy(next_status)

last_word_pro_dict = copy.deepcopy(last_word_dict)
next_word_pro_dict = copy.deepcopy(next_word_dict)

for i in last_word_dict:
    last_word_pro_dict[i] /= msr_number_dict[i[-2]][head_dict[i[-1]]]

for i in next_word_dict:
    next_word_pro_dict[i] /= msr_number_dict[i[0]][head_dict[i[1]]]

print('特征学习完成！')

print('正在分词...')
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