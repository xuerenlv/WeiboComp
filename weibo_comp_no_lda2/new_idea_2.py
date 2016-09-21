# coding:utf8
'''
Created on 2016年9月13日

@author: Xuehj
'''
from utils_about_weibo_3 import read_lable, read_status
import codecs
from tutils_about_weibo import determine_one_word_is_location, \
    tran_loc_to_request
import random
import sys
import math
from sklearn import svm

reload(sys)  
sys.setdefaultencoding('utf8') 


dictionry = {}
loc_map_twotypes_data = {}
loc_map_twotypes_clf = {}
test_predict_result = {}

inverse_doc_fre = {}
def gen_inverse_documen_fre():
    print "calc inverse document frequency---start"
    

    weibo_list_train = []
    weibo_list_test = []

    status_map_train = read_status()  # train
    for uid in status_map_train:
        content_concated = " ".join([ one_con_li[4] for one_con_li in status_map_train[uid]])
        weibo_list_train.append(content_concated)

    weibo_map_test = read_status(file_name='test/test_status.txt')
    for uid in weibo_map_test:
        content_concated = " ".join([ one_con_li[4] for one_con_li in weibo_map_test[uid]])
        weibo_list_test.append(content_concated)
    
    
    all_weibo = []
    all_weibo.extend(weibo_list_train)
    all_weibo.extend(weibo_list_test)
    N = len(weibo_list_test) + len(weibo_list_train)
    
    global inverse_doc_fre
    for one_weibo in all_weibo:
        for one_word in set(one_weibo.split(' ')):
            inverse_doc_fre[one_word] = 1.0 + inverse_doc_fre.get(one_word, 0.0)
    for one_word in inverse_doc_fre:
        inverse_doc_fre[one_word] = math.log(float(N) / inverse_doc_fre[one_word])
    print "calc inverse document frequency---end"



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



def gen_test_predict_result_use_PINGLV():
    read_wordmap()
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
                
                for occur_loc in occur_loc_list:
                    # 初始化 大容器
                    if occur_loc not in loc_map_twotypes_data:
                        loc_map_twotypes_data[occur_loc] = {}
                        loc_map_twotypes_data[occur_loc][0] = 0.0
                        loc_map_twotypes_data[occur_loc][1] = 1.0
                        
#                     print this_vec
                    if occur_loc == loc:
                        loc_map_twotypes_data[occur_loc][1] += 1.0
                    else:
                        loc_map_twotypes_data[occur_loc][0] += 1.0        
    print "-- construct data for train -- end"    
    
    print "test data predict -- start"
    test_status = read_status(file_name='test/test_status.txt')
    for uid in test_status:
        weibo_list = test_status[uid]
        true_loc_dic = {}
        oriloc_list = []
        
        for one_weibo in weibo_list:
            one_weibo_content = one_weibo[4]
            occur_loc_list = process_one_weibo_return_loclist_original(one_weibo_content)
            
             
            if len(occur_loc_list) != 0:
                for one_loc in occur_loc_list:
                    trust_val = 1.0
                    if one_loc in loc_map_twotypes_data:  
                        trust_val = loc_map_twotypes_data[one_loc][1] / (loc_map_twotypes_data[one_loc][0] + loc_map_twotypes_data[one_loc][1])
                    oriloc_list.append(one_loc + "-" + str(trust_val))
                    request_loc = tran_loc_to_request(one_loc)
                    true_loc_dic[request_loc] = true_loc_dic.get(request_loc, 0.0) + trust_val  
        
        if len(true_loc_dic) != 0:
            
            max_val = -1.0;
            max_loc = ""
            for one_loc in true_loc_dic:
                if true_loc_dic[one_loc] > max_val:
                    max_val = true_loc_dic[one_loc]
                    max_loc = one_loc
            
            test_predict_result[uid] = max_loc
        
        one_p_line = ""
        for i in true_loc_dic:
            one_p_line += " " + str(i) + ":" + str(true_loc_dic[i])
        
        print "ori_loc :", ' '.join(oriloc_list)
        print "transform_loc :", one_p_line[1:]
        print "uid : ", uid, ' predict loc: ', test_predict_result.get(uid, '---')
    print "test data predict -- end"
    
    pass




def gen_test_predict_result():
    print "test data predict -- start"
    test_status = read_status(file_name='test/test_status.txt')
    for uid in test_status:
        weibo_list = test_status[uid]
        true_loc_list = []
        
        for one_weibo in weibo_list:
            one_weibo_content = one_weibo[4]
            occur_loc_list = process_one_weibo_return_loclist_original(one_weibo_content)
            if len(occur_loc_list) != 0:
                for one_loc in occur_loc_list:
                    one_weibo_vec = train_vecdic_to_vec(gen_vector_for_one_weibo(one_weibo_content))
                    
                    if predit_oneloc_with_oneweibo(one_loc, one_weibo_vec):
                        true_loc_list.append(tran_loc_to_request(one_loc))
        
        if len(true_loc_list) != 0:
            test_predict_result[uid] = pick_location_this(true_loc_list)
        
        print "uid : ", uid, ' predict loc: ', test_predict_result[uid]
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



def predit_oneloc_with_oneweibo(one_loc, one_weibo_vec):
    if one_loc not in loc_map_twotypes_clf:
        return True
    
    predict_result = loc_map_twotypes_clf[one_loc].predict(one_weibo_vec)[0]
    if predict_result == 1.0:
        return True
    else:
        return False



def read_wordmap():
    with open("word_map.txt", 'r') as fr:
        for one_line in fr.readlines():
            dictionry[one_line[:-1]] = len(dictionry) + 11
    return dictionry

def gen_vector_for_one_weibo(one_weibo_content):
    global dictionry
#     vec = [0.0 for i in range(len(dictionry))]
    vec_dic = {}  # 稀疏矩阵表示
    words_list = one_weibo_content.split(" ")
    for one_word in words_list:
        if one_word in dictionry:
            vec_dic[dictionry[one_word]] = inverse_doc_fre[one_word] * (float(words_list.count(one_word)) / len(words_list))
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
                        loc_map_twotypes_data[occur_loc][0] = []
                        loc_map_twotypes_data[occur_loc][1] = []
                        
                        loc_map_twotypes_clf[occur_loc] = {}
                        
#                     print this_vec
                    if occur_loc == loc:
                        loc_map_twotypes_data[occur_loc][1].append(this_vec)
                    else:
                        loc_map_twotypes_data[occur_loc][0].append(this_vec)        
    print "-- construct data for train -- end"    
    
    print "--print data size -- start"
    for one_loc in loc_map_twotypes_data:
        print 'location :', one_loc, " true size: ", len(loc_map_twotypes_data[one_loc][1]), " false size: ", len(loc_map_twotypes_data[one_loc][0])
    print "--print data size -- end"
    
    print "-- train the clf model -- start"
    for index, one_loc in enumerate(loc_map_twotypes_clf.keys()):
        
        print 'location :', one_loc, " true size: ", len(loc_map_twotypes_data[one_loc][1]), " false size: ", len(loc_map_twotypes_data[one_loc][0]), " index: ", index, " all: ", len(loc_map_twotypes_clf.keys())
        
        lable_list = []
        data_list = []
        max_size = max([len(loc_map_twotypes_data[one_loc][1]), len(loc_map_twotypes_data[one_loc][0])])
        loc_map_twotypes_data[one_loc][1].extend(select_x_this(loc_map_twotypes_data[one_loc][1], max_size - len(loc_map_twotypes_data[one_loc][1])))
        loc_map_twotypes_data[one_loc][0].extend(select_x_this(loc_map_twotypes_data[one_loc][0], max_size - len(loc_map_twotypes_data[one_loc][0])))
        
        lable_list = [0.0 for i in range(len(loc_map_twotypes_data[one_loc][0]))]
        lable_list.extend([1.0 for i in range(len(loc_map_twotypes_data[one_loc][1]))])
        
        data_list = loc_map_twotypes_data[one_loc][0]
        data_list.extend(loc_map_twotypes_data[one_loc][1])
        
        
        X = []
        for one_dic_vec in data_list:
            X.append(train_vecdic_to_vec(one_dic_vec))
        
#         print data_list
#         print 'location :',one_loc,"one loc train data size: ",len(data_list)," lable size: ",len(lable_list)
#         from sklearn.ensemble import RandomForestClassifier
#         clf = RandomForestClassifier(n_estimators=5, n_jobs=-1)
#         clf = clf.fit(X, lable_list)
        
        clf = svm.LinearSVC()
        clf.fit(X,lable_list)
#         pre_label = clf.predict(p_X)
        
        
        loc_map_twotypes_clf[one_loc] = clf
    print "-- train the clf model -- end"    
    
    
    
    pass



# 为了类别平均
def select_x_this(ori_list, se_size):
    if len(ori_list) == 0:
        ori_list.append({})
    if se_size == 0:
        return []

    se_list = []
    while len(se_list) < se_size:
        ind = int(random.random() * (len(ori_list) - 1))
        se_list.append(ori_list[ind])

    return se_list

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
    gen_inverse_documen_fre()
    for_train()
    gen_test_predict_result()
    
    
#     gen_test_predict_result_use_PINGLV()
    evaluate()
    pass
