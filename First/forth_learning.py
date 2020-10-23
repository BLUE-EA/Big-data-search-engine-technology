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

# 第四步特征计算

msr_number_dict_txt = open('msr_number_dict.txt', 'r', encoding='utf-8')
msr_number_dict = eval(msr_number_dict_txt.read())
msr_number_dict_txt.close()

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

# print(last_word_dict)

last_word_pro_dict = copy.deepcopy(last_word_dict)
next_word_pro_dict = copy.deepcopy(next_word_dict)

for i in last_word_dict:
    # try:
    last_word_pro_dict[i] /= msr_number_dict[i[-2]][head_dict[i[-1]]]
    # except BaseException:
    #     continue

for i in next_word_dict:
    # try:
    next_word_pro_dict[i] /= msr_number_dict[i[0]][head_dict[i[1]]]
    # except BaseException:
    #     continue

# print(last_word_dict['人们'])

# print(last_word_dict)
# print(next_word_dict)
print(last_word_pro_dict['特殊E'])
# print(next_word_pro_dict)

last_word_dict_txt = open('last_word_dict.txt', 'w', encoding='utf-8')
last_word_dict_txt.write(str(last_word_dict))
last_word_dict_txt.close()

next_word_dict_txt = open('next_word_dict.txt', 'w', encoding='utf-8')
next_word_dict_txt.write(str(next_word_dict))
next_word_dict_txt.close()

last_word_pro_dict_txt = open('last_word_pro_dict.txt', 'w', encoding='utf-8')
last_word_pro_dict_txt.write(str(last_word_pro_dict))
last_word_pro_dict_txt.close()

next_word_pro_dict_txt = open('next_word_pro_dict.txt', 'w', encoding='utf-8')
next_word_pro_dict_txt.write(str(next_word_pro_dict))
next_word_pro_dict_txt.close()

print(next_word_pro_dict)
print('第四步完成')