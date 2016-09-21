# coding:utf8
'''
Created on 2016年7月25日

@author: Xuehj
'''
import codecs
from tutils_about_weibo import tranform_loc, tranfiorm_age

############################################################################################
###############
###############     主要用于读取 训练集 的数据 
###############
############################################################################################

# 读取 info
def read_info(file_name='train/train_info.txt'):
    info_map = {}
    with codecs.open(file_name, 'r', 'utf8') as fr:
        for one_line in fr.readlines():
            one_line_split = one_line[:-1].split('||')
#             print one_line_split
            uid = one_line_split[0]
            nickname = one_line_split[1]
            nick_url = one_line_split[2]
            
            if uid not in info_map:
                info_map[uid] = {}
            info_map[uid]['nick_name'] = nickname
            info_map[uid]['nick_url'] = nick_url 
#     print info_map
    return info_map
    

# 读取 label
def read_lable(file_name='train/train_labels.txt'):
    label_map = {}
    with codecs.open(file_name, 'r', 'utf8') as fr:
        for one_line in fr.readlines():
            one_line_split = one_line[:-1].split('||')
            
            uid = one_line_split[0]
            sex = one_line_split[1]
            age = int(one_line_split[2])
            loc = one_line_split[3].split(' ')[0]
            
            if loc != u'None':
                loc = tranform_loc(loc)
            
#             print one_line_split, loc
            
            if uid not in label_map:
                label_map[uid] = {}
            label_map[uid]['sex'] = sex
            label_map[uid]['age'] = age
            label_map[uid]['loc'] = loc 
#     print label_map
    return label_map


# 读取 links 
def read_links(file_name='train/train_links.txt'):
    links_map = {}
    with codecs.open(file_name, 'r', 'utf8') as fr:
        for one_line in fr.readlines():
            one_line_split = one_line[:-1].split(' ')
            uid = one_line_split[0]
            fans = one_line_split[1:]
            
            if uid not in links_map:
                links_map[uid] = []
            links_map[uid].extend(fans)
#     print links_map
    return links_map            


# 读取 status 
def read_status(file_name='train/train_status.txt'):
    weibo_map = {}
    with codecs.open(file_name, 'r', 'utf8') as fr:
        for one_line in fr.readlines():
            one_line_split = one_line[:-2].split(',')
            
            if len(one_line_split) < 5:
                continue
            
            uid = one_line_split[0]
            zhuanfa_num = one_line_split[1]
            pinglu_num = one_line_split[2]
            laiyuan = one_line_split[3]
            c_time = one_line_split[4]
            content = one_line_split[5]
#             print one_line
#             print uid, zhuanfa_num, pinglu_num, laiyuan, c_time, content
            if uid not in weibo_map:
                weibo_map[uid] = []
            weibo_map[uid].append([zhuanfa_num, pinglu_num, laiyuan, c_time, content])
#     print weibo_map['2218057087']
    return weibo_map



if __name__ == '__main__':
#     read_info()
#     read_lable()
    read_links('test/test_links.txt')
#     read_status('test/test_status.txt')
    pass
