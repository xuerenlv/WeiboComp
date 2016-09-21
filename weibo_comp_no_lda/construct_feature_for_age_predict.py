# coding:utf8
'''
Created on 2016年8月6日

@author: Xuehj
'''
from tutils_about_weibo import tranfiorm_age
from utils_about_weibo_3 import read_lable, read_links, read_status


def get_unique_source(weibo_map):
    unique_source = {}
    for uid in weibo_map:
        for one_weibo in weibo_map[uid]:
            source = one_weibo[2]
            if source not in unique_source:
                unique_source[source] = 1
            
    return unique_source.keys()

unique_source_list = get_unique_source(read_status())



def feature_construct_for_train(label_map, links_map, weibo_map):
    
    target_lable = []
    feature_list = []
    
    for uid in label_map:
        target_lable.append(tranfiorm_age(int(label_map[uid]['age'])))
        
        this_feature = []
        
        # 第一个特征，有多少个粉丝
        this_feature.append(len(links_map.get(uid, [1])))
        
        # 第2，微博数
        weibo_num = len(weibo_map.get(uid, [1]))
        this_feature.append(weibo_num)
        
        # 微博重复数
        unique_source = {}
        unique_weibo = {}
        
        source_num = {}
        for one_weibo in weibo_map[uid]:
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
        feature_list.append(this_feature)
    
    
    return target_lable, feature_list



def feature_construct_for_teat(links_map, weibo_map):
    feature_map = {}
    
    for uid in weibo_map:
        this_feature = []
        
        # 第一个特征，有多少个粉丝
        this_feature.append(len(links_map.get(uid, [1])))
        
        # 第2，微博数
        weibo_num = len(weibo_map.get(uid, [1]))
        this_feature.append(weibo_num)
        
        # 微博重复数
        unique_source = {}
        unique_weibo = {}
        
        source_num = {}
        for one_weibo in weibo_map[uid]:
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
    
        feature_map[uid] = this_feature
    
    return feature_map


def train_and_predict_age():
    target_lable, feature_list = feature_construct_for_train(read_lable(), read_links(), read_status())
    
    feature_map = feature_construct_for_teat(read_links(file_name='test/test_links.txt'), read_status(file_name='test/test_status.txt'))
    
    
    from sklearn.ensemble import RandomForestClassifier
    clf = RandomForestClassifier(n_estimators=10)
    clf = clf.fit(feature_list, target_lable)
    
    
    pre_result = {}
    for uid in feature_map:
        pre_result[uid] = clf.predict(feature_map[uid])[0]
        
        
    return pre_result
    
    
    


if __name__ == '__main__':
    
    
    
    
    
    pass
