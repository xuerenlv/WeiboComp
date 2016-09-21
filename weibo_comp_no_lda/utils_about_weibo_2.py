# coding:utf8
'''
Created on 2016年7月25日

@author: Xuehj
'''
import codecs
from utils_about_weibo_3 import read_lable, read_status
from tutils_about_weibo import tranfiorm_age
import random

############################################################################################
###############
###############    根据 微博文本，微博来源 的用词习惯 
###############
############################################################################################



# 返回 词语分别在男性微博中的出现数量，和在女性微博中的中的出现数量
def read_train_weibo_status(label_map, weibo_map):
    
    f_map_word_count_content = {}
    m_map_word_count_content = {}
    
    f_map_word_count_source = {}
    m_map_word_count_source = {}

    mail_weibo_list = []
    fmail_weibo_list = []
    for uid in weibo_map:
        if uid not in label_map:
            continue
        
        sex = label_map[uid]['sex']
        weibo_list = weibo_map[uid]
        new_weibo_list = []
         
        # 去除 重复的微博
        rem_content = {}
        for one_weibo in weibo_list:
            source = one_weibo[2]
            content = one_weibo[4]
            
            if  source+content not in rem_content:
                new_weibo_list.append(one_weibo)
                rem_content[source+content]=1
         
        weibo_list = new_weibo_list
        if sex == u'm':
            mail_weibo_list.append(weibo_list)
        else:
            fmail_weibo_list.append(weibo_list)
    
    # 为了 样本的平衡 进行采样
    append_weibo_list = []
    for iter in range(len(mail_weibo_list) - len(fmail_weibo_list)):
        ran = random.random()
        append_weibo_list.append(fmail_weibo_list[int(ran * len(fmail_weibo_list))])
    fmail_weibo_list.extend(append_weibo_list)
    
    for weibo_list in mail_weibo_list:
        for one_weibo in weibo_list:
            source = one_weibo[2]
            content = one_weibo[4]
            for one_word in filter_source_and_content_list(source.split(' ')):
                if len(one_word) < 2:
                    continue
                m_map_word_count_source[one_word] = m_map_word_count_source.get(one_word, 0) + 1
            for one_word in filter_source_and_content_list(content.split(' ')):
                if len(one_word) < 2:
                    continue
                m_map_word_count_content[one_word] = m_map_word_count_content.get(one_word, 0) + 1
    
    for weibo_list in fmail_weibo_list:
        for one_weibo in weibo_list:
            source = one_weibo[2]
            content = one_weibo[4]
            for one_word in filter_source_and_content_list(source.split(' ')):
                if len(one_word) < 2:
                    continue
                f_map_word_count_source[one_word] = f_map_word_count_source.get(one_word, 0) + 1
            for one_word in filter_source_and_content_list(content.split(' ')):
                if len(one_word) < 2:
                    continue
                f_map_word_count_content[one_word] = f_map_word_count_content.get(one_word, 0) + 1
    
#     print len(mail_weibo_list),len(fmail_weibo_list)
        
    
    return m_map_word_count_content, f_map_word_count_content, m_map_word_count_source, f_map_word_count_source



# 对一条微博内容进行过滤，去除其中无意义的部分
def filter_source_and_content_list(source_or_content_list):
    
#     filter_list = [u'', u'！', u'-', u']', u'[', u'？', u'，', u'。', u'#', u'丶', u'【', u'】', u'（', u')']
#     filter_list_2 = [u'：', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'', u'']
    return [w for w in source_or_content_list if len(w) > 1]





# 这里的假设是各年龄段的用词不一样
def read_train_weibo_status_for_age(label_map, weibo_map):
    
    before_79_map_word_count_source = {}
    in_80_to_89__map_word_count_source = {}
    past_90__map_word_count_source = {}
    
    before_79_map_word_count_content = {}
    in_80_to_89__map_word_count_content = {}
    past_90__map_word_count_content = {}
    
    count____before_79_map_word_weibo_num = 0.0
    count____in_80_to_89__map_word_weibo_num = 0.0
    count____past_90__map_word_weibo_num = 0.0
    
    
    before_79_weibo_list = []
    in_80_to_89_weibo_list = []
    past_90_weibo_list = []
    
    
    for uid in weibo_map:
        if uid not in label_map:
            continue
        this_age = tranfiorm_age(int(label_map[uid]['age']))
        weibo_list = weibo_map[uid]
        
        if this_age == u'-1979':
            before_79_weibo_list.append(weibo_list)
        elif this_age == u"1980-1989":
            in_80_to_89_weibo_list.append(weibo_list)
        else:
            past_90_weibo_list.append(weibo_list)
    
    max_list_size = max(len(before_79_weibo_list),len(in_80_to_89_weibo_list),len(past_90_weibo_list))
    
    append_weibo_list = []
    for iter in range(max_list_size - len(before_79_weibo_list)):
        ran = random.random()
        append_weibo_list.append(before_79_weibo_list[int(ran * len(before_79_weibo_list))])
    before_79_weibo_list.extend(append_weibo_list)
    
    append_weibo_list = []
    for iter in range(max_list_size - len(in_80_to_89_weibo_list)):
        ran = random.random()
        append_weibo_list.append(in_80_to_89_weibo_list[int(ran * len(in_80_to_89_weibo_list))])
    in_80_to_89_weibo_list.extend(append_weibo_list)
    
    append_weibo_list = []
    for iter in range(max_list_size - len(past_90_weibo_list)):
        ran = random.random()
        append_weibo_list.append(past_90_weibo_list[int(ran * len(past_90_weibo_list))])
    past_90_weibo_list.extend(append_weibo_list)
   
    for weibo_list in before_79_weibo_list:
        for one_weibo in weibo_list:
            source = one_weibo[2]
            content = one_weibo[4]
            
            for one_word in filter_source_and_content_list(source.split(' ')):
                if len(one_word) < 2:
                    continue                 
                before_79_map_word_count_source[one_word] = before_79_map_word_count_source.get(one_word, 0) + 1
                
            for one_word in filter_source_and_content_list(content.split(' ')):
                if len(one_word) < 2:
                    continue                 
                before_79_map_word_count_content[one_word] = before_79_map_word_count_content.get(one_word, 0) + 1
    
    for weibo_list in in_80_to_89_weibo_list:
        for one_weibo in weibo_list:
            source = one_weibo[2]
            content = one_weibo[4]
            
            for one_word in filter_source_and_content_list(source.split(' ')):
                if len(one_word) < 2:
                    continue                 
                in_80_to_89__map_word_count_source[one_word] = in_80_to_89__map_word_count_source.get(one_word, 0) + 1
                
            for one_word in filter_source_and_content_list(content.split(' ')):
                if len(one_word) < 2:
                    continue                 
                in_80_to_89__map_word_count_content[one_word] = in_80_to_89__map_word_count_content.get(one_word, 0) + 1
                
    for weibo_list in past_90_weibo_list:
        for one_weibo in weibo_list:
            source = one_weibo[2]
            content = one_weibo[4]
            
            for one_word in filter_source_and_content_list(source.split(' ')):
                if len(one_word) < 2:
                    continue                 
                past_90__map_word_count_source[one_word] = past_90__map_word_count_source.get(one_word, 0) + 1
                
            for one_word in filter_source_and_content_list(content.split(' ')):
                if len(one_word) < 2:
                    continue                 
                past_90__map_word_count_content[one_word] = past_90__map_word_count_content.get(one_word, 0) + 1            

    
#     for word in before_79_map_word_count_source.keys():
#         before_79_map_word_count_source[word] = float(before_79_map_word_count_source[word]) / count____before_79_map_word_weibo_num
#     for word in in_80_to_89__map_word_count_source.keys():
#         in_80_to_89__map_word_count_source[word] = float(in_80_to_89__map_word_count_source[word]) / count____in_80_to_89__map_word_weibo_num
#     for word in past_90__map_word_count_source.keys():
#         past_90__map_word_count_source[word] = float(past_90__map_word_count_source[word]) / count____past_90__map_word_weibo_num
#     
#     for word in before_79_map_word_count_content.keys():
#         before_79_map_word_count_content[word] = float(before_79_map_word_count_content[word]) / count____before_79_map_word_weibo_num
#     for word in in_80_to_89__map_word_count_content.keys():
#         in_80_to_89__map_word_count_content[word] = float(in_80_to_89__map_word_count_content[word]) / count____in_80_to_89__map_word_weibo_num
#     for word in past_90__map_word_count_content.keys():
#         past_90__map_word_count_content[word] = float(past_90__map_word_count_content[word]) / count____past_90__map_word_weibo_num
    
#     print len(before_79_map_word_count_source)
#     print len(in_80_to_89__map_word_count_source)
#     print len(past_90__map_word_count_source)
#      
#     print len(before_79_map_word_count_content)
#     print len(in_80_to_89__map_word_count_content)
#     print len(past_90__map_word_count_content)
    
    return before_79_map_word_count_source, in_80_to_89__map_word_count_source, past_90__map_word_count_source, before_79_map_word_count_content, in_80_to_89__map_word_count_content, past_90__map_word_count_content
    pass







if __name__ == '__main__':
#     read_train_weibo_status(read_lable(), read_status())
    read_train_weibo_status_for_age(read_lable(), read_status())
    pass
