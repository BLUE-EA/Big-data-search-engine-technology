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

# 第三步特征计算：计算一个字的状态变化概率

msr_number_dict_txt = open('msr_number_dict.txt', 'r', encoding='utf-8')
msr_number_dict = eval(msr_number_dict_txt.read())
msr_number_dict_txt.close()
msr_pro_dict_txt = open('msr_pro_dict.txt', 'r', encoding='utf-8')
msr_pro_dict = eval(msr_pro_dict_txt.read())
msr_pro_dict_txt.close()

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

msr_double_array_dict_txt = open('msr_double_array_dict.txt', 'w', encoding='utf-8')
msr_double_array_dict_txt.write(str(msr_double_array_dict))
msr_double_array_dict_txt.close()

msr_double_array_pro_dict_txt = open('msr_double_array_pro_dict.txt', 'w', encoding='utf-8')
msr_double_array_pro_dict_txt.write(str(msr_double_array_pro_dict))
msr_double_array_pro_dict_txt.close()

print(msr_double_array_dict)
print(msr_double_array_pro_dict)
print('第三步执行完成')