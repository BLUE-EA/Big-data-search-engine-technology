import copy

msr_training_utf8 = open('msr_training.utf8.ic', 'r', encoding='utf-8-sig')
msr_str = msr_training_utf8.read()
msr_training_utf8.close()
msr_list = msr_str.split('\n')

# str_temp = msr_list[0][1]+msr_list[0][2]+msr_list[0][3]

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

# temp_array = open('count_dict.txt', 'w', encoding='utf-8')
# temp_array.write(str(count_dict))
# temp_array.close()

print(count_dict)
print('第一步执行完成')