# coding:utf8
'''
Created on 2016年9月14日

@author: Xuehj
'''

import sys
import codecs
from tutils_about_weibo import tran_loc_to_request, \
    determine_one_word_is_location
from utils_about_weibo_3 import read_status
import numpy as np
import math

reload(sys)  
sys.setdefaultencoding('utf8') 





dictionry = {}
loc_map_twotypes_data = {}



test_predict_result = {}
def evaluate():
    print "-- evaluate -- start"
    loc_right = 0.0
    loc_yitian = 0.0

    with codecs.open('test_nolabels_result.txt', 'r', 'utf8') as fr:
        for one_line in fr.readlines():
            one_line_sp = one_line[:-1].split(',')
            uid = one_line_sp[0]
            loc = one_line_sp[2].split(' ')[0]
        
            if uid in test_predict_result:
                if tran_loc_to_request(loc) == test_predict_result[uid]:
                    loc_right += 1.0
                loc_yitian += 1.0
                
    print "loc_yitian: ", loc_yitian, " loc_right: ", loc_right
    pass



def gen_test_predict_result():
    print "test data predict -- start"
    test_status = read_status(file_name='test/test_status.txt')
    for uid in test_status:
        weibo_list = test_status[uid]
        
        true_loc_dic = {}
        
        for one_weibo in weibo_list:
            one_weibo_content = one_weibo[4]
            occur_loc_list = process_one_weibo_return_loclist_original(one_weibo_content)
            
            if len(occur_loc_list) != 0:
                one_weibo_vec = normalize(np.array(train_vecdic_to_vec(gen_vector_for_one_weibo(one_weibo_content))))
                for one_loc in occur_loc_list:
                    true_loc_dic[one_loc] = 0.5
                    if one_loc in loc_map_twotypes_data:
#                         true_loc_dic[one_loc] = max(true_loc_dic.get(one_loc, 0.0) , ((one_weibo_vec * loc_map_twotypes_data[one_loc][1]).sum() + 1.0) / ((one_weibo_vec * loc_map_twotypes_data[one_loc][1]).sum() + 1.0 + (one_weibo_vec * loc_map_twotypes_data[one_loc][0]).sum()))
                        true_loc_dic[one_loc] = true_loc_dic.get(one_loc, 0.0) + (one_weibo_vec * loc_map_twotypes_data[one_loc][1]).sum() - (one_weibo_vec * loc_map_twotypes_data[one_loc][0]).sum()
#                         print true_loc_dic[one_loc],(one_weibo_vec * loc_map_twotypes_data[one_loc][1]).sum(),(one_weibo_vec * loc_map_twotypes_data[one_loc][0]).sum()
                    else:
                        true_loc_dic[one_loc] =  0.8
#         if len(true_loc_list) != 0:
#             test_predict_result[uid] = pick_location_this(true_loc_list)
#         true_loc_for_pick = {}
#         for one_loc in true_loc_dic:
#             true_loc_for_pick[tran_loc_to_request(one_loc)] = true_loc_for_pick.get(tran_loc_to_request(one_loc),0.0) + true_loc_dic[one_loc] 
        
        requested_true_loc = {}
        for loc in true_loc_dic:
            if tran_loc_to_request(loc) not in requested_true_loc:
                requested_true_loc[tran_loc_to_request(loc)] = 0.0
            requested_true_loc[tran_loc_to_request(loc)] += true_loc_dic[loc]
        
        if len(requested_true_loc) !=0:
            max_val = -1.0;
            max_loc  = ""
            for one_loc in requested_true_loc:
                if requested_true_loc[one_loc] > max_val:
                    max_val = requested_true_loc[one_loc]
                    max_loc = one_loc
            
            test_predict_result[uid] = max_loc
        
#             print "uid : ", uid, ' predict loc: ', test_predict_result[uid]
    print "test data predict -- end"
    pass


# 从一个list中选出出现次数大于半数的地名
def pick_location_this(loc_list):
#     print "size: ",len(set(loc_list))
#     max_count = max([loc_list.count(w) for w in set(loc_list)])
    for loc in loc_list:
        if loc_list.count(loc) >= len(loc_list) / 2:
            return loc
    return loc_list[0]




def read_wordmap():
    with open("word_map.txt", 'r') as fr:
        for one_line in fr.readlines():
            dictionry[one_line[:-1]] = len(dictionry) + 11
    return dictionry

def gen_vector_for_one_weibo(one_weibo_content):
    global dictionry
#     vec = [0.0 for i in range(len(dictionry))]
    vec_dic = {}  # 稀疏矩阵表示
    for one_word in one_weibo_content.split(" "):
        if one_word in dictionry:
            vec_dic[dictionry[one_word]] = vec_dic.get(dictionry[one_word], 0.0) + 1.0
    return vec_dic

def train_vecdic_to_vec(vec_dic):
    vec = [0.0 for i in range(len(dictionry))]
    for i in vec_dic:
        vec[i] = vec_dic[i] 
    return vec


def for_train():
    status_map_train = read_status()  # train
    lable_train = read_lable_original_for_loc()
    
    print "-- construct data for train -- start"
    for uid in lable_train:
        weibo_list = status_map_train[uid]
        loc = lable_train[uid]['loc']
        
        for one_weibo in weibo_list:
            weibo_content = one_weibo[4]
            
            occur_loc_list = process_one_weibo_return_loclist_original(weibo_content)
            if len(occur_loc_list) != 0:
                this_vec = gen_vector_for_one_weibo(weibo_content)
                
                for occur_loc in occur_loc_list:
                    # 初始化 大容器
                    if occur_loc not in loc_map_twotypes_data:
                        loc_map_twotypes_data[occur_loc] = {}
                        loc_map_twotypes_data[occur_loc][0] = np.array([0.0 for i in range(len(dictionry))])
                        loc_map_twotypes_data[occur_loc][10] = 1.0
                        loc_map_twotypes_data[occur_loc][1] = np.array([0.0 for i in range(len(dictionry))])
                        loc_map_twotypes_data[occur_loc][11] = 1.0
                        
                    
                    for i in this_vec:
                        if occur_loc == loc:
                            loc_map_twotypes_data[occur_loc][1][i] += this_vec[i]
                            loc_map_twotypes_data[occur_loc][11] += 1.0
                        else:
                            loc_map_twotypes_data[occur_loc][0][i] += this_vec[i]
                            loc_map_twotypes_data[occur_loc][10] += 1.0        
    
    for one_loc in loc_map_twotypes_data:
        loc_map_twotypes_data[one_loc][0] = loc_map_twotypes_data[one_loc][0]/loc_map_twotypes_data[occur_loc][10]
        loc_map_twotypes_data[one_loc][1] = loc_map_twotypes_data[one_loc][1]/loc_map_twotypes_data[occur_loc][11]
        print loc_map_twotypes_data[one_loc][0].sum()
    
    print "-- construct data for train -- end"    
 
# 归一化
def normalize(vec):
    mo = math.sqrt((vec*vec).sum())
    return vec/mo

    
# 处理一条微博，返回其中可用的地址信息
def process_one_weibo_return_loclist_original(weibo_content):
    loc_list = []
    words_list = weibo_content.split(' ')
    for index, one_word in enumerate(words_list):
        if len(one_word) <= 1:
            continue
        
        if u'湖南' == one_word and index + 1 < len(words_list) and words_list[index + 1] == u'卫视':
            continue
        if u'北京' == one_word and u'春晚' in words_list:
            continue
        
#         盛 淮南
        if u'淮南' == one_word and u'盛' in words_list:
            continue
        
        if one_word[-1] == u'省' or one_word[-1] == u'市':
            one_word = one_word[:-1]
        if one_word[0] == u'@':
            one_word = one_word[1:]
        # ****************************************************
        if u'·' in one_word:
            one_word = one_word[:one_word.find(u'·')]
        if len(one_word) == 3 and one_word[:-1] == u"人":
            one_word = one_word[:-1]
        # ****************************************************
            
        if determine_one_word_is_location(one_word):
            loc_list.append(one_word)
    return loc_list

# 读取 label
def read_lable_original_for_loc(file_name='train/train_labels.txt'):
    label_map = {}
    with codecs.open(file_name, 'r', 'utf8') as fr:
        for one_line in fr.readlines():
            one_line_split = one_line[:-1].split('||')
            
            uid = one_line_split[0]
            sex = one_line_split[1]
            age = int(one_line_split[2])
            
            loc_ori = one_line_split[3].split(' ')
            this_loc = ""
            if loc_ori[0] in (u'北京', u'上海', u'天津', u'重庆'):
                this_loc = loc_ori[0]
            else:
                this_loc = loc_ori[1]
            
            if this_loc == ' None':
                continue
            
            
#             print one_line_split, loc
            
            if uid not in label_map:
                label_map[uid] = {}
            label_map[uid]['sex'] = sex
            label_map[uid]['age'] = age
            label_map[uid]['loc'] = this_loc 
            
#     print label_map
    return label_map















if __name__ == '__main__':
    
    read_wordmap()
    for_train()
    gen_test_predict_result()
    evaluate()
    pass
