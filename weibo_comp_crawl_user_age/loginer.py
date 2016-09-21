# -*- coding: utf-8 -*-

'''
Created on 2015-08-20

@author: xhj
'''

import traceback
from my_log import WeiboSearchLog
from Queue import Queue
import threading
import sys
import time
from _random import Random
import random
try:
    import os, errno
    from login import login
    import cookielib
    import urllib2

    from login import do_login
except:
    s = traceback.format_exc()
    print s


class Loginer:
    # 用于存放 登陆用户 ，username与password
    username_pawword_list = []

    # 用于存放cookie
    cookies_list = []
    cookies_list_mutex = threading.Lock()

    # 用于存放代理
    proxy_list = []
    proxy_list_mutex = threading.Lock()


    per_proxy_used_most = 0

    def __init__(self):
        pass

    # 从存放cookie的文件中获取cookie信息
    def get_cookie_from_file(self, cookie_file):
        cookie = {}
        with open(cookie_file) as f:
            lines = f.readlines()
        for line in lines[1:]:
            line = line.strip()
            space_index = line.find(' ')
            pair = line.split(';')[0][space_index:]
            pair = pair.replace('\"', '')
            equal_index = pair.find('=')
            key = pair[:equal_index]
            value = pair[equal_index + 1:]
            cookie[key] = value
        return cookie

    # 填充 username_pawword_list
    def fill_username_pawword_list(self):
        from config_operation import LOGIN_USER_INFOR as user_info_list
        for login_info in user_info_list:
            one_user = []
            one_user.append(login_info['username'])
            one_user.append(login_info['password'])
            Loginer.username_pawword_list.append(one_user)
        pass

    # 当 cookies_list 为空的时候，对其进行填充
    def fill_cookies_list(self):
        if len(Loginer.username_pawword_list)==0 :
            self.fill_username_pawword_list()

        login_info = Loginer.username_pawword_list[0]
        username = login_info[0]
        password = login_info[1]
        del Loginer.username_pawword_list[0]

        cookie_file = 'cookies/weibo_login_cookies_' + username + '.dat'
        if do_login(username, password, cookie_file) == 1:
            WeiboSearchLog().get_scheduler_logger().info(username + "--login success !")
            Loginer.cookies_list.append(self.get_cookie_from_file(cookie_file))
        else:
            WeiboSearchLog().get_scheduler_logger().warning(username + "--login failed !")
        pass

    # 当 proxy_list 为空的时候，对其进行填充
    def fill_proxy_list(self):
        from config_operation import PROXIES as proxy_info_list
        for proxy in proxy_info_list:
            Loginer.proxy_list.append(proxy)

    # 删除 cookie_list 中的一个cookie信息
    def del_cookie(self):
        Loginer.cookies_list_mutex.acquire()
        if len(Loginer.cookies_list) > 0:
            del Loginer.cookies_list[-1]
            WeiboSearchLog().get_scheduler_logger().warning("  --change cookie ! cookie size: " + str(len(Loginer.cookies_list)))
            time.sleep(int(20))
        Loginer.cookies_list_mutex.release()

    # 抓取失败时，先换proxy，当所有的proxy换完时，换账号
    def del_proxy(self):
        Loginer.proxy_list_mutex.acquire()
        if Loginer.per_proxy_used_most<50: ##一个代理没有使用150次，不可以进行删除
            Loginer.proxy_list_mutex.release()
            return
        Loginer.per_proxy_used_most = 0
        if len(Loginer.proxy_list) > 0:
            del Loginer.proxy_list[-1]
            WeiboSearchLog().get_scheduler_logger().warning("  --change proxy ! proxy size: " + str(len(Loginer.proxy_list)))
            time.sleep(int(20))
        if len(Loginer.proxy_list) == 0:
            self.del_cookie()
            time.sleep(int(20))
        Loginer.proxy_list_mutex.release()

    # 获取cookie信息
    def get_cookie(self):
        Loginer.cookies_list_mutex.acquire()
        if len(Loginer.cookies_list) > 0:
            Loginer.cookies_list_mutex.release()
            return Loginer.cookies_list[-1]
        else:
            self.fill_cookies_list()
            if len(Loginer.cookies_list) > 0:
                re = Loginer.cookies_list[-1]
                Loginer.cookies_list_mutex.release()
                return re
            else:
                WeiboSearchLog().get_scheduler_logger().error("ALL user login failed,the ip .....")
                sys.exit(1)

    # 获取代理信息
    def get_proxy(self):
        Loginer.proxy_list_mutex.acquire()
        Loginer.per_proxy_used_most += 1
        re = ""
        if len(Loginer.proxy_list) > 0:
            re = Loginer.proxy_list[-1]
        else:
            self.fill_proxy_list()
            Loginer.per_proxy_used_most = 0
            re = Loginer.proxy_list[-1]
        Loginer.proxy_list_mutex.release()

        #  当一个proxy用了超过100次的时候，删除
        if Loginer.per_proxy_used_most > 150:
            self.del_proxy()

        return re





if __name__ == '__main__':
    loginer = Loginer()
    print loginer.get_proxy()
    print loginer.get_cookie()
