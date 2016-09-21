# -*- coding: utf-8 -*-
import pymongo
try:
    import sys
    import yaml
    import os
except ImportError:
    print >> sys.stderr
    sys.exit()

try:
    curpath=os.path.normpath( os.path.join( os.getcwd(), os.path.dirname(__file__) ) ) 
    conf_file = open(curpath+"/config.yaml", 'r')
except:
    try:
        conf_file = open("../config.yaml", 'r')
    except:
        print 'weibo.yaml not found'
    
conf_dic = yaml.load(conf_file)
conf_file.close()

LOGIN_USER_INFOR = []
for login_infor in conf_dic['login']:
    LOGIN_USER_INFOR.append({"username":str(login_infor["username"]), "password":str(login_infor["password"])})    

PROXIES = []
for proxy in conf_dic['proxies']:
    PROXIES.append(proxy['ip'])

DBNAME = conf_dic['searchdb']['dbname']
DB_HOST = conf_dic['searchdb']['host']
DB_PORT = conf_dic['searchdb']['port']



if __name__ == '__main__':
    print "x"
    client = pymongo.MongoClient(DB_HOST, DB_PORT)[DBNAME]
    print client.name
#     print len(LOGIN_USER_INFOR)
#     for login_infor in LOGIN_USER_INFOR:
#         print 'username: ' + login_infor['username'] + '\t' + "password: " + login_infor['password']
#     
#     print len(PROXIES)
#     for proxy in PROXIES:
#         print 'IP',proxy
