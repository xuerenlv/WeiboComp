# -*- coding: utf-8 -*-

'''
Created on 2015-08-21

@author: xhj
'''
from craw_page_parse import crawl_real_time_with_keyword, \
    crawl_set_time_with_keyword, crawl_set_time_with_keyword_and_nickname
# from craw_page_parse import  crawl_set_time_with_only_keyword
import os
import logging.config
import random
import datetime
from crawl_comment_from_db import crawl_comment, crawl_repost
from craw_page_parse_2 import crawl_uid_from_nickname, \
    crawl_userinfo_from_uname_or_uid, crawl_userinfo_2_from_uid
from store_model import UserInfo_store, Single_weibo_with_more_info_store, \
    Bie_Ming_store, Weibo_url_to_Comment_url, Single_comment, \
    Single_comment_store, Weibo_url_to_repost_url, Single_repost_store

from urllib import quote_plus
from mongoengine.context_managers import switch_collection
from mongoengine.queryset.visitor import Q



if not os.path.exists('logs/'):
    os.mkdir('logs')
if os.path.exists('logs/scheduler.log'):
    open('logs/scheduler.log', 'w').truncate()

curpath = os.path.normpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) 
logging.config.fileConfig(curpath + '/runtime_infor_log.conf')

if not os.path.exists('data/'):
    os.mkdir('data')
if not os.path.exists('cookies/'):
    os.mkdir('cookies')


# 抓取实时的微博，现在还不需要
def crawl_real_time_main(key_words_list):
    thrads_list = []
    for i in range(len(key_words_list)):
        thrads_list.append(crawl_real_time_with_keyword(key_words_list[i], 'real_time_' + str(i)))
    return thrads_list

# 按照天数，分别创建开始url  
# 关键词，对应微博很多，按天抓取
def crawl_set_time_main_many(key_word, start_time, end_time, how_many_days_one_thread, how_many_days_crawl_once):
    thrads_list = []
    while start_time <= end_time:
        end_2 = start_time + datetime.timedelta(days=how_many_days_one_thread-1)
        thrads_list.append(crawl_set_time_with_keyword(key_word, start_time, end_2, how_many_days_crawl_once, 'crawl_settime_thread' + str(start_time) + " to " + str(end_2)))
        start_time = end_2+datetime.timedelta(days=1)
    return thrads_list


# 不按天抓取,一次抓取全部
# 给定： 关键词，开始时间，结束时间，用户list
def crawl_set_time_main_little(key_word, start_time, end_time, nickname_list):
    thrads_list = []
    for nickname in nickname_list:
        thrads_list.append(crawl_set_time_with_keyword_and_nickname(key_word, start_time, end_time, nickname, nickname + "_thread"))
    return thrads_list
    


# 从 数据库 中已转换的 comment url 中 提取url，然后进行抓取
def crawl_comment_from_fie():
    #  从单独的微博文件中读取信息
    
    all_thrads_list = []
    
    # 读出数据
    list_contains_set_weibourl_and_commenturl = []
    global Weibo_url_to_Comment_url
    for one_entry in Weibo_url_to_Comment_url.objects:
        list_contains_set_weibourl_and_commenturl.append((one_entry['weibo_url'], one_entry['comment_url']))
    
    one_piece = len(list_contains_set_weibourl_and_commenturl) / 12
    for i in range(12):
        all_thrads_list.append(crawl_comment(list_contains_set_weibourl_and_commenturl[i * one_piece:(i + 1) * one_piece], 'crawl_comment___' + str(i)))
        
    for thread in all_thrads_list:
        thread.start()
    for thread in all_thrads_list:
        thread.join()

# 抓取用户 转发
def crawl_repost_from_db():
    all_thrads_list = []
    
    # 读出数据
    list_contains_set_weibourl_and_reposturl = []
    global Weibo_url_to_repost_url
    for one_entry in Weibo_url_to_repost_url.objects:
        list_contains_set_weibourl_and_reposturl.append((one_entry['weibo_url'], one_entry['repost_url']))
    
    random.shuffle(list_contains_set_weibourl_and_reposturl)
    one_piece = len(list_contains_set_weibourl_and_reposturl) / 12
    for i in range(12):
        all_thrads_list.append(crawl_repost(list_contains_set_weibourl_and_reposturl[i * one_piece:(i + 1) * one_piece], 'crawl_repost___' + str(i)))
        
    for thread in all_thrads_list:
        thread.start()
    for thread in all_thrads_list:
        thread.join()
    pass

    

# 抓取一个关键词下所有的微博；也可以抓取一个 hashtag 下所有的微博，但是要修改相应的 初始url
def crawl_one_keyword():
    all_thrads_list = []
    key_word = '转基因'
    start_time = datetime.datetime(2016, 2, 16)
    end_time = datetime.datetime(2016, 2, 26)    
    all_thrads_list.extend(crawl_set_time_main_many(key_word, start_time, end_time, how_many_days_one_thread=1, how_many_days_crawl_once=1))    
    for thread in all_thrads_list:
        thread.start()
    for thread in all_thrads_list:
        thread.join() 

# 抓取一个 hashtag 下所有的微博
# def crawl_hash_tag():
#     all_thrads_list = []
#     key_word = '四六级成绩'
#     start_time = datetime.datetime(2015, 12, 10)
#     end_time = datetime.datetime(2015, 12, 31) 
# 
#     how_many_days_one_thread = 5
#     while start_time + datetime.timedelta(days=how_many_days_one_thread) < end_time:
#         end_2 = start_time + datetime.timedelta(days=how_many_days_one_thread)
#         all_thrads_list.append(crawl_set_time_with_only_keyword(key_word, start_time, end_2, 'crawl_settime_thread' + str(start_time) + " to " + str(end_2)))
#         start_time = end_2
#     if start_time < end_time:
#         all_thrads_list.append(crawl_set_time_with_only_keyword(key_word, start_time, end_time, 'crawl_settime_thread' + str(start_time) + " to " + str(end_time)))    
#     for thread in all_thrads_list:
#         thread.start()
#     for thread in all_thrads_list:
#         thread.join()    

# 抓取特定用户下的微博，抓取特别媒体关于末个关键词的微博
def crawl_set_user_weibo_about_keyword():
    all_thrads_list = []
    key_word = '扶老人'
    start_time = datetime.datetime(2011, 1, 1)
    end_time = datetime.datetime(2015, 9, 6)
    nickname_list = ["新闻晨报", "南方都市报", "广州日报", "南方日报", "环球时报", "扬子晚报", "新京报", "每日经济新闻", "楚天都市报"]
    all_thrads_list.extend(crawl_set_time_main_little(key_word, start_time, end_time, nickname_list))
    for thread in all_thrads_list:
        thread.start()
    for thread in all_thrads_list:
        thread.join() 


####################################################################################### crawl userinfo start
# 通过用户的uid来抓取用户信息，，抓取任务中的一个需要
def chuli_nickname_crawl_userinfo():
    uid_or_uname_list = []
#     uid_or_uname_list = read_data_from_database_for___uid_or_uname_list()
    
    with open("test_nolabels.txt") as file_r:
        for one_line in file_r.readlines():
            uid_or_uname_list.append(one_line[:-2])
    print len(uid_or_uname_list)
    
    how_many_uids_one_thread = len(uid_or_uname_list) / 10
    
    all_thrads_list = []
    start = 0
    end = how_many_uids_one_thread
    count = 0
    while end < len(uid_or_uname_list):
        all_thrads_list.append(crawl_userinfo_2_from_uid(uid_or_uname_list[start:end], "crawl_userinfo_from_uname_or_uid_" + str(count)))
        start = start + how_many_uids_one_thread
        end = end + how_many_uids_one_thread
        count = count + 1
    if start < len(uid_or_uname_list):
        all_thrads_list.append(crawl_userinfo_2_from_uid(uid_or_uname_list[start:len(uid_or_uname_list)], "crawl_userinfo_from_uname_or_uid_" + str(count)))
     
    for thread in all_thrads_list:
        thread.start()
    for thread in all_thrads_list:
        thread.join()  

# 从数据库中取出已经爬取的用户信息的 uid 与 nickname
def read_data_from_database_uids_and_nicknames():
    uids_and_nicknames = []
    for one_user_info in UserInfo_store.objects:
        uids_and_nicknames.append(one_user_info["uid_or_uname"])
        uids_and_nicknames.append(one_user_info["nickname"])
    return uids_and_nicknames

# 处理数据库中的 at_info
def chuli_at_info(at_info):
    nickname_list = []
    for one in at_info.split("[fen_ge]"):
        nickname_list.append(one[:one.find(":")])    
    return nickname_list

# def read_alread_crawled_uids_or_nicknames():
#     alread_crawled_uids_or_nicknames = []
#     fr = open("data/already_crawled_uids_or_nicknames.txt","r")
#     for one_line in fr.readlines():
# #         alread_crawled_uids_or_nicknames.append(one_line[:-1])
#         pass
#     fr.close()
#     return alread_crawled_uids_or_nicknames

# def write_alread_crawled_uids_or_nicknames(alread_crawled_uids_or_nicknames):
#     fw = open("data/already_crawled_uids_or_nicknames.txt","a")
#     for one_thing in alread_crawled_uids_or_nicknames:
#         fw.write(one_thing+"\n")
#     fw.close()


# 从数据库中读出数据构造 uid_or_uname_list
def read_data_from_database_for___uid_or_uname_list():
    uid_or_uname_list = []
    
    this_uid_list = []
    this_nickname_list = []
    
    weibo_collection_name = []
#     weibo_collection_name = ["zhuanjiyin_nohashtag_original_2014_03_01_to_2014_03_10_detmine_1", \
#                        "zhuanjiyin_nohashtag_original_2014_03_10_to_2014_03_20_detmine_2", \
#                        "zhuanjiyin_nohashtag_original_2014_03_20_to_2014_04_01_detmine_3"]

    # 处理微博中的用户信息
    print "start single weibo"
    global Single_weibo_with_more_info_store
    for one_collection in weibo_collection_name:
        with switch_collection(Single_weibo_with_more_info_store, one_collection) as Single_weibo_with_more_info_store:
            for one_weibo in Single_weibo_with_more_info_store.objects:
                this_uid_list.append(one_weibo["uid"])
                this_uid_list.append(one_weibo["come_from_user_id"])
                this_nickname_list.extend(chuli_at_info(one_weibo["at_info"]))
                this_nickname_list.extend(chuli_at_info(one_weibo["retweet_reason_at_info"]))
    
    # 处理 comment 中的用户信息
    # 'zhuanjiyin_nohashtag_original_single_comment_2016_with_more_info'
    print "start comment"
    comment_collections = []
#     comment_collections.append('zhuanjiyin_nohashtag_original_single_comment_2014_with_more_info_repair')
    
    global Single_comment_store
    for one_collection in comment_collections:
        with switch_collection(Single_comment_store, one_collection) as Single_comment_store:
            for one_comment in Single_comment_store.objects:
                this_uid_list.append(one_comment["uid"])
                this_nickname_list.extend(chuli_at_info(one_comment["at_info"]))
                
    print "start repost"
    repost_collections = []
    repost_collections.append("zhuanjiyin_nohashtag_original_single_repost_2016_with_more_info_repair")

    global Single_repost_store
    for one_collection in repost_collections:
        with switch_collection(Single_repost_store, one_collection) as Single_repost_store:
            for one_comment in Single_repost_store.objects:
                this_uid_list.append(one_comment["uid"])
                this_nickname_list.extend(chuli_at_info(one_comment["at_info"]))
                
                
    uid_or_uname_list.extend(list(set(this_uid_list)))
    uid_or_uname_list.extend(list(set(this_nickname_list)))
    uid_or_uname_list = list(set(uid_or_uname_list))
#     print "start filter"
#     for uid_or_nickname in set(this_uid_list):    
#         if len(UserInfo_store.objects(Q(uid_or_uname=str(uid_or_nickname)) | Q(nickname=str(uid_or_nickname)))) == 0 or\
#          len(Bie_Ming_store.objects(Q(uid_or_uname=str(uid_or_nickname)) | Q(bie_ming=str(uid_or_nickname)))) == 0:
#             uid_or_uname_list.append(uid_or_nickname)
#             
#     for uid_or_nickname in set(this_nickname_list) :
#         if len(UserInfo_store.objects(Q(uid_or_uname=str(uid_or_nickname)) | Q(nickname=str(uid_or_nickname)))) == 0 or\
#          len(Bie_Ming_store.objects(Q(uid_or_uname=str(uid_or_nickname)) | Q(bie_ming=str(uid_or_nickname)))) == 0:
#             uid_or_uname_list.append(uid_or_nickname)

    random.shuffle(uid_or_uname_list)
    print len(uid_or_uname_list)
    return uid_or_uname_list

####################################################################################### crawl userinfo end


# 通过抓取页面，把nickname转换成uid或者在微博的标示，，，这个是中间的一个需要
def main_2_just_tran_nickname_to_uidoruname():
    file_r = open("100_atname_file.txt", 'r')
    
    nickname_list = []
    for line in file_r.readlines():
        op_nickname = line[line.find('nickname:'):]
        nickname = op_nickname[op_nickname.find(':') + 1:op_nickname.rfind(']')]
        nickname_list.append(nickname)
    
    all_thrads_list = []
    start = 0
    end = 10
    count = 1
    while end < len(nickname_list):
        all_thrads_list.append(crawl_uid_from_nickname(nickname_list[start:end], "crawl_uid_from_nickname_" + str(count)))
        start += 10
        end += 10
        count += 1
    if(start < len(nickname_list)):
        all_thrads_list.append(crawl_uid_from_nickname(nickname_list[start:len(nickname_list)], "crawl_uid_from_nickname_" + str(count)))

    for thread in all_thrads_list:
        thread.start()
    for thread in all_thrads_list:
        thread.join()  

###################################################################################### start 1
# 用query expansion ，抓取相应词语的微博。

# key_word_list : 存放query expansion的keyword
# start_time : datetime对象，开始时间   end_time ： datetime对象，结束时间
def crawl_keywords_list(key_word_list, start_time, end_time):
    all_thrads_list = []
    for key_word in key_word_list:
        all_thrads_list.extend(crawl_set_time_main_many(key_word, start_time, end_time, 110))    
    for thread in all_thrads_list:
        thread.start()
    for thread in all_thrads_list:
        thread.join()  

# 读文件，构造keywordslist ，这个是 query expansion 的抓取
def gen_keywords_list():
    # 已操作文件： 1 
    file_r = open('./query_expansion_three_word/result_three_word_0.txt', 'r')
    start_time = ""
    end_time = ""
    count = 1
    key_words_list = []
    for line in file_r.readlines():
        if count == 1:
            line = line[:-1].split(' ')
            start_time = datetime.datetime(int(line[0]), int(line[1]), int(line[2]))
        elif count == 2:
            line = line[:-1].split(' ')
            end_time = datetime.datetime(int(line[0]), int(line[1]), int(line[2]))
        else:
            key_words_list.append(line[:line.find('-')])  
        count += 1
    return (key_words_list, start_time, end_time)
###################################################################################### end 1


if __name__ == '__main__':    
#     key_words_list,start_time,end_time=gen_keywords_list()
#     crawl_keywords_list(key_words_list, start_time, end_time)
    
    # 对于一个关键词，抓取特定时间段的微博（hashtag 也可以）
#     crawl_one_keyword()
    
    # 抓取用户评论，通过已转换好的 comment url
#     crawl_comment_from_fie()
    
    # 抓取用户转发，通过已转换好的 repost url
    
#     crawl_repost_from_db() 
    
    # 从数据库中，读取 uid 昵称 之类，然后去抓取用户信息
    chuli_nickname_crawl_userinfo()

    # 抓取特定用户，关于特定关键词的微博     
#     crawl_set_user_weibo_about_keyword()
  
    pass  
   
   
   
   
   
   
   
   
   
   
   
   
   
   
