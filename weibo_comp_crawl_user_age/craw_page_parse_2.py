# -*- coding: utf-8 -*-

'''
Created on 2015-08-21

@author: xhj
'''
import requests
import StringIO
import gzip
import threading
from loginer import Loginer
import time
from my_log import WeiboSearchLog
import os
import traceback
from bs4 import BeautifulSoup


import re
from Queue import Queue
import datetime
from store_model import Single_weibo_store, UserInfo, UserInfo_store, \
    UserInfo_loc, UserInfo_loc_store, Bie_Ming_store
from mongoengine.errors import NotUniqueError
import random
from craw_page_parse import Crawler_with_proxy, crawl_set_time_with_keyword

import sys  
from urllib import quote, quote_plus
from mongoengine.queryset.visitor import Q
reload(sys)  
sys.setdefaultencoding('utf8')   





# # 通过 nickname 抓取 uid
class crawl_uid_from_nickname(threading.Thread):  
    file_write_lock = threading.Lock()
    
    def __init__(self, nicknam_list, thread_name='crawl_uid_from_nickname'):
        threading.Thread.__init__(self)
        self.nickname_list = nicknam_list

        self.url_queue = Queue()
        self.second_url_queue = Queue() 
        pass
    
#     http://weibo.cn/search/user/?keyword=孔庆东&page=1
    def init_url_queue(self):
        for nickname in self.nickname_list:
            url = "http://weibo.cn/search/user/?keyword=" + nickname + "&page=1"
            self.url_queue.put(url)
        pass
        
    # 抓取并解析页面
    def crawl(self, url, is_again=True):
        loginer = Loginer()
        cookie = loginer.get_cookie()
        proxy = loginer.get_proxy()
        craw_object = Crawler_with_proxy(url, cookie, proxy)
        
        WeiboSearchLog().get_scheduler_logger().info(self.name + " start to crawl ! " + url)
        
        uid_or_uname = ""
        try:
            page = craw_object.get_page()
            
            uid_or_uname = page_parser_from_search_for_uid(page)
        except:
            print traceback.format_exc()
            crawl_set_time_with_keyword.del_proxy_lock.acquire()
            if proxy == loginer.get_proxy():
                loginer.del_proxy()
                WeiboSearchLog().get_scheduler_logger().warning(self.name + " proxy exception , change proxy !")
            crawl_set_time_with_keyword.del_proxy_lock.release()
            if is_again:
                return self.crawl(url, is_again=False)
            else:
                self.second_url_queue.put(url)
                return uid_or_uname
        return uid_or_uname
    
    def run(self):
        self.init_url_queue()
        while not self.url_queue.empty() or not self.second_url_queue.empty():
            url = ""
            if not self.url_queue.empty():
                url = self.url_queue.get()
            else:
                url = self.second_url_queue.get()
            uid_or_uname = self.crawl(url)
            op_url = url[url.find("keyword="):]
            nickname = op_url[op_url.find('=') + 1:op_url.find('&')]
            
            crawl_uid_from_nickname.file_write_lock.acquire()
            file_w = open("at_nickname_to_(uid_or_uname).txt", 'a')
            file_w.write("[uid_or_uname:" + uid_or_uname + "][nickname:" + nickname + "]" + '\n')
            file_w.flush()
            file_w.close()
            crawl_uid_from_nickname.file_write_lock.release()
        pass  


# # 通过 uid_or_uname 抓取 用户信息 
class crawl_userinfo_from_uname_or_uid(threading.Thread):  
    
    def __init__(self, uid_or_uname_list, thread_name='crawl_userinfo_from_uname_or_uid'):
        threading.Thread.__init__(self, name=thread_name)
        self.uid_or_uname_list = uid_or_uname_list

        self.url_queue = Queue()
        self.second_url_queue = Queue() 
        pass
    
#     http://weibo.cn/breakingnews?f=search_0
    def init_url_queue(self):
        global UserInfo_store
        for uid_or_nickname in self.uid_or_uname_list:            
#             if len(UserInfo_store.objects(Q(uid_or_uname=str(uid_or_nickname)) | Q(nickname=str(uid_or_nickname)))) != 0 or\
#             len(Bie_Ming_store.objects(Q(uid_or_uname=str(uid_or_nickname)) | Q(bie_ming=str(uid_or_nickname)))) != 0:
#                 continue
           
            self.url_queue.put(uid_or_nickname)
        print "crawl size ::::::::: ",self.url_queue.qsize()
        pass
        
    # 抓取并解析页面
    def crawl(self, uid_or_nickname, is_again=False):
        
        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        url = ''
#         if len(UserInfo_store.objects(Q(uid_or_uname=str(uid_or_nickname)) | Q(nickname=str(uid_or_nickname)))) != 0 or\
#             len(Bie_Ming_store.objects(Q(uid_or_uname=str(uid_or_nickname)) | Q(bie_ming=str(uid_or_nickname)))) != 0:
#             WeiboSearchLog().get_scheduler_logger().info("already in the database : " + uid_or_nickname)
#             return "nothing"
        
        quote_uid_or_nickname = ""
        try:
            quote_uid_or_nickname = quote_plus(str(uid_or_nickname.strip()))
        except:
            print  traceback.format_exc()
            print  uid_or_nickname
        
        url = "http://weibo.cn/" + uid_or_nickname + "/info"
            
#         if quote_uid_or_nickname == uid_or_nickname:
#             url = "http://weibo.cn/" + uid_or_nickname + "?f=search_0"
#         else:
#             url = "http://weibo.cn/n/" + quote_uid_or_nickname
        
        # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        
        loginer = Loginer()
        cookie = loginer.get_cookie()
        proxy = loginer.get_proxy()
        
        craw_object = Crawler_with_proxy(url, cookie, proxy)
        
        WeiboSearchLog().get_scheduler_logger().info(self.name + " start to crawl ! " + url)
        
        user_info = ""
        try:
            page = craw_object.get_page()
            
            user_info = page_parser_from_search_for_UserInfo(page, url)
        except:
            if is_again:
                return self.crawl(url, is_again=False)
            else:
                return user_info
            
            
        return user_info
    
    
#     uid_or_uname = StringField(unique=True)
#     nickname = StringField()
#     is_persion = StringField()
#     check_or_not = StringField()
#     fensi = StringField()
    
    def store_userinfo_to_db(self, uid_or_nickname, user_info):
        if type(user_info) is str:
            WeiboSearchLog().get_scheduler_logger().info(self.name + " nothing ! :" + user_info)
            return
        
        unique_user_info = UserInfo_store(uid_or_uname=user_info.uid_or_uname, nickname=user_info.nickname, is_persion=user_info.is_persion, check_or_not=user_info.check_or_not, fensi=user_info.fensi,
                                          sex=user_info.sex, location=user_info.location,
                                          check_info=user_info.check_info,
                                          weibo_all_nums=user_info.weibo_all_nums,
                                          guan_zhu_nums=user_info.guan_zhu_nums
                                          )
        
#         Bie_Ming_store
        if unique_user_info['uid_or_uname'] != uid_or_nickname:
            bie_ming = Bie_Ming_store(uid_or_uname=unique_user_info['uid_or_uname']  , bie_ming=uid_or_nickname)
        
        sign = 0
        try:
            unique_user_info.save()
        except NotUniqueError:
            sign = 1
            WeiboSearchLog().get_scheduler_logger().info(self.name + " insert to database, not unique ! " + unique_user_info['uid_or_uname'] + " crawl: " + uid_or_nickname)
        except:
            sign = 2
            WeiboSearchLog().get_scheduler_logger().info(self.name + " insert to database, something wrong !")
        
        if sign == 0:
            WeiboSearchLog().get_scheduler_logger().info(self.name + " insert to database, success success success success!")
        
        try:
            bie_ming.save()
        except NotUniqueError:
            WeiboSearchLog().get_scheduler_logger().info(self.name + " bieming already in database" + unique_user_info['uid_or_uname'] + " crawl: " + uid_or_nickname)
            return
        except:
            WeiboSearchLog().get_scheduler_logger().info(self.name + " bieming insert to database, something wrong !")
            return
        
        pass
    
    
    def run(self):
        self.init_url_queue()
        while not self.url_queue.empty() or not self.second_url_queue.empty():
            uid_or_nickname = ""
            if not self.url_queue.empty():
                uid_or_nickname = self.url_queue.get()
            else:
                uid_or_nickname = self.second_url_queue.get()
            user_info = self.crawl(uid_or_nickname)
#             print user_info.to_string()
            if not  user_info == "nothing" :
                self.store_userinfo_to_db(uid_or_nickname, user_info)
        pass  





# # 通过 uid_or_uname 抓取 用户信息 (位置信息)
class crawl_userinfo_2_from_uid(threading.Thread):  
    
    def __init__(self, uid_or_uname_list, thread_name='crawl_userinfo_from_uname_or_uid'):
        threading.Thread.__init__(self)
        self.uid_or_uname_list = uid_or_uname_list

        self.url_queue = Queue()
        self.second_url_queue = Queue() 
        pass
    
#     http://weibo.cn/1806760610/info
    def init_url_queue(self):
        for uid_or_nickname in self.uid_or_uname_list:
            url = "http://weibo.cn/" + uid_or_nickname + "/info"
            self.url_queue.put(url)
        pass
        
    # 抓取并解析页面
    def crawl(self, url, is_again=True):
        loginer = Loginer()
        cookie = loginer.get_cookie()
        proxy = loginer.get_proxy()
        craw_object = Crawler_with_proxy(url, cookie, proxy)
        
        WeiboSearchLog().get_scheduler_logger().info(self.name + " start to crawl ! " + url)
        
        user_info_loc = ""
        try:
            page = craw_object.get_page()
            
            user_info_loc = page_parser_from_search_for_UserInfoLoc(page, url)
        except:
            print traceback.format_exc()
            crawl_set_time_with_keyword.del_proxy_lock.acquire()
            if proxy == loginer.get_proxy():
                loginer.del_proxy()
                WeiboSearchLog().get_scheduler_logger().warning(self.name + " proxy exception , change proxy !")
            crawl_set_time_with_keyword.del_proxy_lock.release()
            if is_again:
                return self.crawl(url, is_again=False)
            else:
                self.second_url_queue.put(url)
                return user_info_loc
        return user_info_loc
    
    
#     uid_or_uname = StringField(unique=True)
#     nickname = StringField()
#     is_persion = StringField()
#     check_or_not = StringField()
#     fensi = StringField()
    
    def store_userinfo_loc_to_db(self, user_info_loc):
        
        unique_user_info_loc = UserInfo_loc_store(uid=user_info_loc.uid, nickname=user_info_loc.nickname, location=user_info_loc.location, sex=user_info_loc.sex, birth=user_info_loc.birth, intro=user_info_loc.intro, check_or_not=user_info_loc.check_or_not, check_info=user_info_loc.check_info)
        try:
            unique_user_info_loc.save()
        except NotUniqueError:
            pass
        except:
            WeiboSearchLog().get_scheduler_logger().info(self.name + " insert to database, something wrong !")
            pass
        WeiboSearchLog().get_scheduler_logger().info(self.name + " insert to database, success !")
        pass
    
    
    def run(self):
        self.init_url_queue()
        while not self.url_queue.empty() or not self.second_url_queue.empty():
            url = ""
            if not self.url_queue.empty():
                url = self.url_queue.get()
            else:
                url = self.second_url_queue.get()
            user_info_loc = self.crawl(url)
#             print user_info.to_string()
            self.store_userinfo_loc_to_db(user_info_loc)
        pass  









############################################  页面解析     ###########################################################

#     http://weibo.cn/1806760610/info
def page_parser_from_search_for_UserInfoLoc(page, url):
    bs_all = BeautifulSoup(page)
    div_all = bs_all.findAll('div', attrs={'class':'c'})

    nickname = ""
    location = ""
    sex = ""
    birth = ""
    intro = ""
    check_or_not = u'否'
    check_info = ""
    op_uid = url[url.find('.cn'):]
    uid = op_uid[op_uid.find('/') + 1:op_uid.rfind('/')]
    for div in div_all:
        for str_in in str(div.getText(u'\n')).split(u'\n'):
            en_str = str_in.encode('utf-8')
            
            if(en_str.startswith(u"昵称")):
                nickname = en_str[en_str.find(':') + 1:]
            elif(en_str.startswith(u"地区")):
                location = en_str[en_str.find(':') + 1:]
            elif(en_str.startswith(u"性别")):
                sex = en_str[en_str.find(':') + 1:]
            elif(en_str.startswith(u"生日")):
                birth = en_str[en_str.find(':') + 1:]
            elif(en_str.startswith(u"简介")):
                intro = en_str[en_str.find(':') + 1:]
            elif(en_str.startswith(u"认证信息")):
                check_or_not = u'是'
                check_info = en_str
    return UserInfo_loc(uid, nickname, location, sex, birth, intro, check_or_not, check_info) 
    
    pass

# http://weibo.cn/1730330447?f=search_0
#     http://weibo.cn/breakingnews?f=search_0
# 解析获取 UserInfo
def page_parser_from_search_for_UserInfo(page, url):
    out_soup = BeautifulSoup(page)
    div_u_first = ""
    for div_u_one in out_soup.findAll('div', attrs={'class':'u'}):
        if u"资料" in div_u_one.getText() and u"私信" in div_u_one.getText():
            div_u_first = div_u_one
            break
    
    # 获取 uid_or_uname,
    uid_or_uname = ""
    for a_one in div_u_first.findAll("a"):
        if u"送Ta会员" in a_one.getText() and u"uid=" in a_one.attrs["href"]:
            a_one_href = a_one.attrs["href"]
            uid_or_uname = a_one_href[a_one_href.find("uid=") + 4:]
            break
    
#     op_url = url[url.find(".cn"):]
#     uid_or_uname = op_url[op_url.find('/')+1:op_url.find('?')]
    
    # 新添加----------------------------------start
    sex = ""
    location = ""
    check_info = ""
    weibo_all_nums = ""
    guan_zhu_nums = ""
    # 新添加----------------------------------end
    
    # is_persion,check_or_not
    is_persion = ""
    check_or_not = ""
    div_class_ut = div_u_first.find('div', attrs={'class':'ut'})
    
    # nickname
    nickname = ""
    span_class_ctt = div_class_ut.findAll('span', attrs={'class':'ctt'})
    for span_class_ctt_one in span_class_ctt:
        span_class_ctt_one_text = span_class_ctt_one.getText() 
        if u"关注" in span_class_ctt_one_text:
            
            if str(span_class_ctt_one_text).find("男") != -1:
                nickname = span_class_ctt_one_text[:span_class_ctt_one_text.find(u'男') - 1]
                sex = "男"
                location = span_class_ctt_one_text[span_class_ctt_one_text.find(u'男') + 2:span_class_ctt_one_text.find(u'关注') - 1]
            if str(span_class_ctt_one_text).find("女") != -1:
                nickname = span_class_ctt_one_text[:span_class_ctt_one_text.find(u'女') - 1]
                sex = "女" 
                location = span_class_ctt_one_text[span_class_ctt_one_text.find(u'女') + 2:span_class_ctt_one_text.find(u'关注') - 1   ]
        if u"认证" in span_class_ctt_one_text:
            check_info = span_class_ctt_one_text[span_class_ctt_one_text.find(u"认证:") + 1:]
            pass
#             op_span_class_ctt_one_html = span_class_ctt_one_html[2:]
#             nickname_candidate = op_span_class_ctt_one_html[op_span_class_ctt_one_html.find('>')+1:op_span_class_ctt_one_html.find('<')]
# #             if str(nickname_candidate).find("男") != -1:
# #                 nickname_candidate = nickname_candidate[:nickname_candidate.find(u'男')-1]
# #             if str(nickname_candidate).find("女") != -1:
# #                 nickname_candidate = nickname_candidate[:nickname_candidate.find(u'女')-1] 
#             nickname = nickname_candidate
    
    
    imag_alt_V = div_class_ut.find('img', attrs={'alt':'V'})
    if imag_alt_V is not None:
        if u"5337" in str(imag_alt_V.attrs['src']):
            is_persion = "no"
        else:
            is_persion = "yes"
        check_or_not = "yes"
    else:
        is_persion = "yes"
        check_or_not = "no"
    
    
    
    # ,fensi
    fensi = ""
    div_tip2_second_leval = div_u_first.find('div', attrs={'class':'tip2'})
    a_all = div_tip2_second_leval.findAll('a')
    for a_one in a_all:
        a_text = a_one.getText()
        if u"粉丝" in a_text:
            fensi = a_text[a_text.find('[') + 1:a_text.find(']')]
        if u"关注" in a_text:
            guan_zhu_nums = a_text[a_text.find('[') + 1:a_text.find(']')]
    
    for span_class_tc in div_tip2_second_leval.findAll('span'):
        span_class_tc_text = span_class_tc.getText()
        if u"微博" in span_class_tc_text:
            weibo_all_nums = span_class_tc_text[span_class_tc_text.find('[') + 1:span_class_tc_text.find(']')]
            
            
    user_info = UserInfo(uid_or_uname, nickname, is_persion, check_or_not, fensi, sex, location, check_info, weibo_all_nums, guan_zhu_nums)
    return user_info
    pass

# #  解析页面，获取搜索的第一个，uid
def page_parser_from_search_for_uid(page):
    out_soup = BeautifulSoup(page)
    table_first = out_soup.find('table')
    td_first = table_first.find('td', attrs={'valign':'top'})
    
    a_href = td_first.find('a').attrs['href']
    
    uid_or_uname = a_href[a_href.rfind('/') + 1:a_href.find('?')] 
    
    return uid_or_uname
