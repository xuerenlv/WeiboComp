# coding:utf8
'''
Created on 2016年7月23日

@author: Xuehj
'''
import os



# 把一个用户 当成 一篇文档
def merge_file(dir_name,file_name):
    
    count = 1
    with open(file_name,'w') as fw:
        for one_file in os.listdir(dir_name):
            print count
            one_line = ""
            with open(dir_name+"/"+one_file,'r') as fr:
                for in_one_line in fr.readlines():
                    one_line+=" "+in_one_line[:-1]

            fw.write(one_line+"\n")
            count+=1
            
            
            pass
    
    pass


if __name__ == '__main__':
    
    merge_file('user_weibo_result', "data_for_gibbs_lda")
    pass