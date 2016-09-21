# coding:utf8

'''
Created on 2016年7月23日

@author: Xuehj
'''
import os



def read_dir(dir_name,file_name):
    with open(file_name,'w') as fw:
        for one_file_name in  os.listdir(dir_name):
            fw.write(one_file_name+"\n")
            pass
    pass


if __name__ == '__main__':
    read_dir("user_weibo_result",'filelist_test.txt')
    pass