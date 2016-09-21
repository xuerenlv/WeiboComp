# coding:utf8
'''
Created on 2016年7月24日

@author: Xuehj
'''
import codecs
from tutils_about_weibo import tran_loc_to_request

if __name__ == '__main__':
    
    with codecs.open("test_nolabels_result.txt", 'r', 'utf8') as file_r:
        with codecs.open("new_test_nolabels_result.txt", 'w', 'utf8') as fw:
            for one_line in file_r.readlines():

                one_line_split = one_line[:-1].split(',')
                uid = one_line_split[0]
                sex = one_line_split[1]
                loc = tran_loc_to_request(one_line_split[2])
                
                print uid,sex,loc
                
                
    pass
