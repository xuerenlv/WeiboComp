# -*- coding: utf-8 -*-

'''
Created on Jan 13, 2016

@author: nlp
'''
from store_model import Single_weibo_with_more_info_store, Single_comment_store, \
    UserInfo_store, Weibo_url_to_Comment_url, Weibo_url_to_repost_url
from mongoengine.context_managers import switch_collection
import traceback

# # [http://weibo.cn/comment/CsfPu1hds?rl=1#cmtfrm][10]  "&page="+str(page_num)
# # ## 读取文件，从文件中获取，微博id，weibo_url，评论数目
# def read_file_fetch_something(weibo_file_name):
# #     file_r = open("single_weibo_from_10_media.txt",'r')
#     file_r = open(weibo_file_name, 'r')
#     dict_url_id = {}
#     
#     for line in file_r.readlines():
#         num_line = line
#         weibo_id = line[line.find(':') + 1:line.find(']')]
# 
#         line = line[line.find('weibo_url'):]
#         line = line[line.find(':') + 1:line.find(']')]
#         weibo_loc = line[line.rfind('/') + 1:]
#         str_first_part = "http://weibo.cn/comment/" + weibo_loc + "?rl=1&page="
#         
#         num_line = num_line[num_line.find('comment_num'):]
#         comment_num = num_line[num_line.find(':') + 1:num_line.find(']')]
#         
#         comment_num_candidate = int(comment_num)
#         if comment_num_candidate > 4000:
#             comment_num = 4000
#         else:
#             comment_num = comment_num_candidate
#         if comment_num < 5:
#             continue
#         yemian_num = comment_num / 10 if comment_num % 10 == 0 else comment_num / 10 + 1 
#         
#         for ye in xrange(1, yemian_num + 1):
#             dict_url_id[str_first_part + str(ye)] = weibo_id
#             
#     return dict_url_id




# 从数据库中提取已抓取到的微博,并写入文件
def main_getobjects_from_db(filename):
    file_w = open(filename, 'a')
    count = 1
    for entry_s in Single_weibo_with_more_info_store.objects:
        str_s = '[' + "id:" + str(count) + ']'
        str_s += '[' + "uid:" + entry_s['uid'] + ']'
        str_s += '[' + "nickname:" + entry_s['nickname'] + ']'
        str_s += '[' + "content:" + entry_s['content'] + ']'
        str_s += '[' + "weibo_url:" + entry_s['weibo_url'] + ']'
        str_s += '[' + "praise_num:" + entry_s['praise_num'] + ']'
        str_s += '[' + "retweet_num:" + entry_s['retweet_num'] + ']'
        str_s += '[' + "comment_num:" + entry_s['comment_num'] + ']'
        str_s += '[' + "creat_time:" + entry_s['creat_time'] + ']'
        file_w.write(str_s + '\n')
        count += 1
    file_w.flush()
    file_w.close()



# 从数据库中提取已抓取到的微博评论,并写入文件
def main_get_comment_from_db():
    file_w = open("apple_phone_single_weibo_comment.txt", 'a')
    for i in xrange(12049, 30967):
        for entry_s in Single_comment_store.objects(weibo_id=str(i)):
            strs = '[' + "weibo_id:" + entry_s['weibo_id'] + ']'
            strs += '[' + "uid:" + entry_s['uid'] + ']'
            strs += '[' + "nickname:" + entry_s['nickname'] + ']'
            strs += '[' + "auth:" + entry_s['auth'] + ']'
            strs += '[' + "content:" + entry_s['content'] + ']'
            strs += '[' + "praise_num:" + entry_s['praise_num'] + ']'
            strs += '[' + "creat_time:" + entry_s['creat_time'] + ']'
            file_w.write(strs + '\n')
    file_w.flush()
    file_w.close()

# 从数据库中提取已抓取到的用户信息,并写入文件    
def main_get_userinfo_from_db():
    file_w = open("user_info_just_this_time.txt", 'a')
    for entry_s in UserInfo_store.objects:
        strs = '[uid_or_uname:' + entry_s['uid_or_uname'] + ']'
        
        nickname_can = entry_s['nickname']
        nickname = nickname_can
        if nickname_can.find(u"男") != -1:
            nickname = nickname_can[:nickname_can.find(u"男") - 1]
        if nickname_can.find(u"女") != -1:
            nickname = nickname_can[:nickname_can.find(u"女") - 1]
        
        strs += '[nickname:' + nickname + ']'
        strs += '[is_persion:' + entry_s['is_persion'] + ']'
        strs += '[verfied_or_not:' + entry_s['check_or_not'] + ']'    
        strs += '[fensi:' + entry_s['fensi'] + ']'  
        file_w.write(strs + '\n')  
    file_w.flush()
    file_w.close()


# 为了抓取微博的评论数据，将数据库中的单条微博进行转换————》weibo_url : weibo comment url
def parse_weibo_to_comment_url():        
    # 对那些 collection 进行操作
    weibo_collection_name = ["zhuanjiyin_nohashtag_original_2014_03_01_to_2014_03_10_detmine_repair_1", \
                        "zhuanjiyin_nohashtag_original_2014_03_11_to_2014_03_20_detmine_repair_2", \
                        "zhuanjiyin_nohashtag_original_2014_03_21_to_2014_03_31_detmine_repair_3"]
    
    
#     weibo_collection_name = ["zhuanjiyin_nohashtag_original_2016_01_27_to_2016_02_05_detmine_repair_1", \
#                           "zhuanjiyin_nohashtag_original_2016_02_06_to_2016_02_15_detmine_repair_2", \
#                           "zhuanjiyin_nohashtag_original_2016_02_16_to_2016_02_26_detmine_repair_3"]    

    global Single_weibo_with_more_info_store
    for one_collection in weibo_collection_name:
        with switch_collection(Single_weibo_with_more_info_store, one_collection) as Single_weibo_with_more_info_store:
            for entry_s in Single_weibo_with_more_info_store.objects:
                weibo_url = entry_s['weibo_url']
                comment_num = entry_s['comment_num']
                if len(comment_num) == 0:
                    continue
                
                weibo_loc = weibo_url[weibo_url.rfind('/') + 1:]
                comment_url_first_part = "http://weibo.cn/comment/" + weibo_loc + "?rl=1&page="
                
                comment_num_candidate = int(comment_num)
                if comment_num_candidate > 4000:
                    comment_num = 4000
                else:
                    comment_num = comment_num_candidate
                if comment_num < 3:
                    continue
                yemian_num = comment_num / 10 if comment_num % 10 == 0 else comment_num / 10 + 1 
        
                for ye in xrange(1, yemian_num + 1):
                    comment_url = comment_url_first_part + str(ye)
                    comment_store = Weibo_url_to_Comment_url(weibo_url=weibo_url, comment_url=comment_url)
                    try:
                        comment_store.save()
                    except:
                        print traceback.format_exc()
                pass
    
    pass 


    
    
# 为了抓取 转发 信息，
def parse_weibo_to_retweet_url():
    # 对那些 collection 进行操作
    weibo_collection_name = ["zhuanjiyin_nohashtag_original_2014_03_01_to_2014_03_10_detmine_repair_1", \
                        "zhuanjiyin_nohashtag_original_2014_03_11_to_2014_03_20_detmine_repair_2", \
                        "zhuanjiyin_nohashtag_original_2014_03_21_to_2014_03_31_detmine_repair_3"]
#     
    
#     weibo_collection_name = ["zhuanjiyin_nohashtag_original_2016_01_27_to_2016_02_05_detmine_repair_1", \
#                           "zhuanjiyin_nohashtag_original_2016_02_06_to_2016_02_15_detmine_repair_2", \
#                           "zhuanjiyin_nohashtag_original_2016_02_16_to_2016_02_26_detmine_repair_3"]    

    global Single_weibo_with_more_info_store
    for one_collection in weibo_collection_name:
        with switch_collection(Single_weibo_with_more_info_store, one_collection) as Single_weibo_with_more_info_store:
            for entry_s in Single_weibo_with_more_info_store.objects:
                weibo_url = entry_s['weibo_url']
                retweet_num = entry_s['retweet_num']
                if len(retweet_num) == 0:
                    continue
                
                weibo_loc = weibo_url[weibo_url.rfind('/') + 1:]
                retweet_num_first_part = "http://weibo.cn/repost/" + weibo_loc + "?rl=1&page="
                
                retweet_num_candidate = int(retweet_num)
                if retweet_num_candidate > 4000:
                    retweet_num = 4000
                else:
                    retweet_num = retweet_num_candidate
                if retweet_num < 3:
                    continue
                yemian_num = retweet_num / 10 if retweet_num % 10 == 0 else retweet_num / 10 + 1 
        
                for ye in xrange(1, yemian_num + 1):
                    retweet_url = retweet_num_first_part + str(ye)
                    retweet_store = Weibo_url_to_repost_url(weibo_url=weibo_url, repost_url=retweet_url)
                    try:
                        retweet_store.save()
                    except:
                        print traceback.format_exc()
                pass
    
    pass 




    
    

    
if __name__ == '__main__':
    
    parse_weibo_to_retweet_url()
    
#     parse_weibo_to_comment_url()
    print "done"
    
#     first = "single_weibo_from_10_media.txt"
#     main_get_comment_from_db()
#     second_name = "4_keyword_2015_1_1_to_2015_9_6.txt"
#     main_getobjects_from_db(second_name)

#     main_get_userinfo_from_db()
#     main_getobjects_from_db("apple_phone_single_weibo.txt")

#     main_getobjects_from_db("fubai_11_07.txt")
    
        
    
#     main_get_comment_from_db()

    pass
    

