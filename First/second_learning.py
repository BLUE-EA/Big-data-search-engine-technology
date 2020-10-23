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

# 特征学习第二步：

count_dict_txt = open('count_dict.txt', 'r', encoding='utf-8')
count_dict = eval(count_dict_txt.read())
count_dict_txt.close()

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

msr_number_dict_txt = open('msr_number_dict.txt', 'w', encoding='utf-8')
msr_number_dict_txt.write(str(msr_number_dict))
msr_number_dict_txt.close()
msr_pro_dict_txt = open('msr_pro_dict.txt', 'w', encoding='utf-8')
msr_pro_dict_txt.write(str(msr_pro_dict))
msr_pro_dict_txt.close()

print(msr_number_dict['殊'])
print(msr_pro_dict['殊'])
print('第二步执行完成')
