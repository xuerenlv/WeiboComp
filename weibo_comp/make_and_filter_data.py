# coding: utf8
'''
Created on 2016年7月24日

@author: Xuehj
'''


def read_some_lines_print(file_name, pre_num):
    
    count = 1
    with open(file_name, 'r') as fr:
        with open(file_name + "_" + str(pre_num) + "_tmp.txt", 'w') as fw:
            for one_ine in fr.readlines():
                if count <= pre_num:
                    print count
                    fw.write(one_ine)
                    count += 1
                else:
                    break
                
    pass





if __name__ == '__main__':
    pass