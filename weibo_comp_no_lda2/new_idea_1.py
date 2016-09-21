# coding:utf8
'''
Created on 2016年9月11日

@author: Xuehj
'''

# old mac needed
# import sys
# sys.path.append('/usr/local/lib/python2.7/site-packages')

from utils_about_weibo_3 import read_status, read_lable, read_links
from tutils_about_weibo import tranfiorm_age

import sys
from sklearn import svm
import random
import math

reload(sys)
sys.setdefaultencoding('utf8')




def get_unique_source(weibo_map):
    unique_source = {}
    for uid in weibo_map:
        for one_weibo in weibo_map[uid]:
            source = one_weibo[2]
            if source not in unique_source:
                unique_source[source] = 1
            
    return unique_source.keys()

unique_source_list = get_unique_source(read_status())

def gen_model_predict_result():
    print "1,construct dataset"
    status_map_train = read_status()  # train
    status_map_test = read_status('test/test_status.txt')  # train

    train_lable_map = read_lable()

    uid_list_train = []
    age_list_train = []
    sex_list_train = []
    loc_list_train = []
    weibo_list_train = []

    uid_list_test = []
    weibo_list_test = []


    others_feature_train = []
    label_map_train = train_lable_map
    links_map_train = read_links()
    weibo_map_train = status_map_train

    for uid in status_map_train:

        content_concated = " ".join([ one_con_li[4] for one_con_li in status_map_train[uid]])
        age = tranfiorm_age(train_lable_map[uid]['age'])
        sex = train_lable_map[uid]['sex']
        loc = train_lable_map[uid]['loc']

        uid_list_train.append(uid)
        age_list_train.append(age)
        sex_list_train.append(sex)
        loc_list_train.append(loc)
        weibo_list_train.append(content_concated)
        
        this_feature = []
        
        # 第一个特征，有多少个粉丝
        this_feature.append(len(links_map_train.get(uid, [1])))
        
        # 第2，微博数
        weibo_num = len(weibo_map_train.get(uid, [1]))
        this_feature.append(weibo_num)
        
        # 微博重复数
        unique_source = {}
        unique_weibo = {}
        
        source_num = {}
        for one_weibo in weibo_map_train[uid]:
            source = one_weibo[2]
            content = one_weibo[4]
            if source not in unique_source:
                unique_source[source] = 1
            if content not in unique_weibo:
                unique_weibo[content] = 1
            
            source_num[source] = source_num.get(source, 0.0) + 1.0
        
        this_feature.append(weibo_num / float(len(unique_source)))
        this_feature.append(weibo_num / float(len(unique_weibo)))
        
        this_list_for_source = []
        for one_source in unique_source_list:
            this_list_for_source.append(source_num[one_source] if one_source in source_num else 0.0)
        this_feature.extend(this_list_for_source)
        
        others_feature_train.append(this_feature)


    links_map_test = read_links(file_name='test/test_links.txt')
    weibo_map_test = read_status(file_name='test/test_status.txt')
    others_feature_test = []
    for uid in status_map_test:

        content_concated = " ".join([ one_con_li[4] for one_con_li in status_map_test[uid]])

        uid_list_test.append(uid)
        weibo_list_test.append(content_concated)
        
        this_feature = []
        
        # 第一个特征，有多少个粉丝
        this_feature.append(len(links_map_test.get(uid, [1])))
        
        # 第2，微博数
        weibo_num = len(weibo_map_test.get(uid, [1]))
        this_feature.append(weibo_num)
        
        # 微博重复数
        unique_source = {}
        unique_weibo = {}
        
        source_num = {}
        for one_weibo in weibo_map_test[uid]:
            source = one_weibo[2]
            content = one_weibo[4]
            if source not in unique_source:
                unique_source[source] = 1
            if content not in unique_weibo:
                unique_weibo[content] = 1
            
            source_num[source] = source_num.get(source, 0.0) + 1.0
        
        this_feature.append(weibo_num / float(len(unique_source)))
        this_feature.append(weibo_num / float(len(unique_weibo)))
    
    
        this_list_for_source = []
        for one_source in unique_source_list:
            this_list_for_source.append(source_num[one_source] if one_source in source_num else 0.0)
    
        this_feature.extend(this_list_for_source)
        others_feature_test.append(this_feature)

#     store_to_file(weibo_list_train, weibo_list_test)
    # one_hot
    all_features_list = gen_feature_list(weibo_list_train, weibo_list_test)
    
    # 添加原始feature
    print "添加原始feature start"
    for index, da in enumerate(others_feature_train):
        all_features_list[index].extend(da) 
    for index, da in enumerate(others_feature_test):
        all_features_list[index + len(others_feature_train)].extend(da)

    X = all_features_list[:len(weibo_list_train)]
    p_X = all_features_list[len(weibo_list_train):]
    print "添加原始feature end"

    print "2,one hot and lda done, start training and predict"
    return train_and_predict(X, age_list_train, p_X, uid_list_test), train_and_predict(X, sex_list_train, p_X, uid_list_test), train_and_predict(X, loc_list_train, p_X, uid_list_test)





# 调用模型进行训练预测
def train_and_predict(raw_X, raw_Y, p_X, uid_list_test):
    pre_map = {}

    print "        t3,reconstructing data"

    lable_map_data = {}
    for one_type in set(raw_Y):
        lable_map_data[one_type] = []
    for da, la in zip(raw_X, raw_Y):
        lable_map_data[la].append(da)

    max_lable_data_sz = 0
    for one_type in lable_map_data:
        if  len(lable_map_data[one_type]) > max_lable_data_sz:
            max_lable_data_sz = len(lable_map_data[one_type])
    for one_type in lable_map_data:
        lable_map_data[one_type].extend(select_x(lable_map_data[one_type], max_lable_data_sz - len(lable_map_data[one_type])))


    X = []
    Y = []
    for one_type in lable_map_data:
        X.extend(lable_map_data[one_type])
        for i in range(len(lable_map_data[one_type])):
            Y.append(one_type)

    print "        t4,start model traing"

#     from sklearn.ensemble import RandomForestClassifier
#     clf = RandomForestClassifier(n_estimators=30, n_jobs=-1)
#     clf = clf.fit(X, Y)
#     pre_label = clf.predict(p_X)

    lin_clf = svm.LinearSVC()
    lin_clf.fit(X,Y)
    pre_label = lin_clf.predict(p_X)

    print "        t5,this done"

    for uid, lable in zip(uid_list_test, pre_label):
        pre_map[uid] = lable

    return pre_map


# 为了类别平均
def select_x(ori_list, se_size):
    print "             start select ", se_size, len(ori_list)
    if se_size == 0:
        return []

    se_list = []
    while len(se_list) < se_size:
        ind = int(random.random() * len(ori_list))
        se_list.append(ori_list[ind])

    print "             select done"
    return se_list



# 接收所有微博，返回 one hot representation
def gen_feature_list(weibo_list_train, weibo_list_test):
    dictiony = {}
    all_weibo = []
    all_weibo.extend(weibo_list_train)
    all_weibo.extend(weibo_list_test)
    for one_weibo in all_weibo:
#         print one_weibo
        for one_word in one_weibo.split(' '):
            if one_word not in dictiony:
                dictiony[one_word] = len(dictiony)
    
    # store word map
#     print "store word map start"
#     with open("word_map.txt",'w') as fw:
#         for one_word in dictiony.keys():
#             fw.write(one_word+"\n")
#     print "store word map end"
    
    print "calc inverse document frequency---start"
    N = len(weibo_list_test) + len(weibo_list_train)
    inverse_doc_fre = {}
    for one_weibo in all_weibo:
        for one_word in set(one_weibo.split(' ')):
            inverse_doc_fre[one_word] = 1.0 + inverse_doc_fre.get(one_word, 0.0)
    for one_word in inverse_doc_fre:
        inverse_doc_fre[one_word] = math.log(float(N) / inverse_doc_fre[one_word])
    print "calc inverse document frequency---end"
    
    
    all_features_list = []
    for one_weibo in all_weibo:
        features = [0.0 for w in range(len(dictiony))]
        one_weibo_words = one_weibo.split(' ')
        one_weibo_len = len(one_weibo_words) 
        for one_word in set(one_weibo_words):
            features[dictiony[one_word]] = inverse_doc_fre[one_word] * (float(one_weibo_words.count(one_word)) / one_weibo_len)
        all_features_list.append(features)

    # 合并lda的结果
    all_theta = read_lda_theta()
    for index, da in enumerate(all_theta):
        all_features_list[index].extend(da)

#     print len(all_features_list[0]),all_features_list[0]
    return all_features_list




# 读取 lda 的训练结果
def read_lda_theta():
    all_theta = []
    with open("lda_theta.txt", 'r') as fr:
        for one_line in fr.readlines():
            all_theta.append([float(w) for w in one_line[:-2].split(' ')])
    return all_theta



# 将微博存储到文件中  用于lda的训练
def store_to_file(weibo_list_train, weibo_list_test):
    with open("train_test_weibo_for_lda.txt", 'w') as fw:
        fw.write(str(len(weibo_list_train) + len(weibo_list_test)) + "\n")
        for one_user_con in weibo_list_train:
            fw.write(one_user_con + "\n")
        for one_user_con in weibo_list_test:
            fw.write(one_user_con + "\n")
    pass


# 将预测结果保存到文件中
def store_predict_result(age_predict_map, sex_predict_map, loc_predict_map):
    store_one_file("age_predict_result.txt", age_predict_map)
    store_one_file("sex_predict_result.txt", sex_predict_map)
    store_one_file("loc_predict_result.txt", loc_predict_map)
    pass

def store_one_file(file_name, predict_map):
    with open(file_name, 'w') as fw:
        for uid in predict_map:
            fw.write(str(uid) + " " + predict_map[uid] + "\n")
    pass


# 读取存到文件中的预测结果
def read_predict_result():
    return read_one_file("age_predict_result.txt"), read_one_file("sex_predict_result.txt"), read_one_file("loc_predict_result.txt")

def read_one_file(file_name):
    st_map = {}
    with open(file_name, 'r') as fr:
        for one_line in fr.readlines():
            uid = one_line[:-2].split(' ')[0]
            lable = one_line[:-2].split(' ')[1]
            st_map[uid] = lable
    return st_map


if __name__ == '__main__':
    age_predict_map, sex_predict_map, loc_predict_map = gen_model_predict_result()
    store_predict_result(age_predict_map, sex_predict_map, loc_predict_map)
    pass
