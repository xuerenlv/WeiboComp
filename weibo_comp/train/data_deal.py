# coding:utf8
'''
Created on 2016年7月21日

@author: Xuehj
'''

import numpy as np

# 读取单个用户的  标签信息
def read_lable(file_name):
    userinfo_dict = {}
    with open(file_name,'r') as fr:
        for one_line in fr.readlines():
            one_line_split = one_line[:-1].split('||') 
            userinfo_dict[one_line_split[0]] = [one_line_split[1],one_line_split[2],one_line_split[3][:one_line_split[3].find(' ')]]
    return userinfo_dict

# 读取单个用户的 粉丝信息
def read_fensi(file_name):
    fensi_dict = {}
    with open(file_name,'r') as fr:
        for one_line in fr.readlines():
            one_line_split = one_line[:-1].split(' ')
            fensi_dict[one_line_split[0]] = [w for w in one_line_split[1:]]
    return fensi_dict

# 读取一条条微博
def read_status(file_name):
    weibo_dict = {}
    with open(file_name,'r') as fr:
        for one_line in fr.readlines():
            one_line_split = one_line[:-1].split(',')
            if one_line_split[0] not in weibo_dict:
                weibo_dict[one_line_split[0]] = [one_line_split[1:]]
            else:
                weibo_dict[one_line_split[0]].append(one_line_split[1:])
    return weibo_dict    
        


# 输出一个用户的 年龄 和 它的 粉丝的平均 年龄
def get_years_and_fensi_years(user_info_dict,fensi_dict):
    
    for one_user in user_info_dict:
        cur_age = user_info_dict[one_user][1]
        
        fensi_li = fensi_dict[one_user] if  one_user in fensi_dict else []
        
        fensi_age = [user_info_dict[one_fensi][1] if one_fensi in user_info_dict  else "-"  for one_fensi in fensi_li ]
        
        fensi_mean_age = np.array([int(fen_age) for fen_age in fensi_age if fen_age != '-']).mean() 
        
        print cur_age,fensi_mean_age
    
    pass




if __name__ == '__main__':
    userinfo_dict = read_lable("train_labels.txt")
    fensi_dict = read_fensi("train_links.txt")
#     weibo_dict = read_status("train_status.txt")
    get_years_and_fensi_years(userinfo_dict,fensi_dict)
    pass