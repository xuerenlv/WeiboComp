# -*- coding: utf-8 -*-
'''
Created on 2016年7月24日

@author: Xuehj
'''



from mongoengine.connection import connect
from mongoengine.document import Document
from mongoengine.fields import StringField
from mongoengine.context_managers import switch_collection


connect("xhj_weibo_comp", host="114.212.86.245", port=int(27017))
#############################   存到mongodb   #############################################
class WeiboResult(Document):
    meta = {'collection': 'weibo_result_1'}
    uid = StringField(unique=True)
    sex = StringField()
    age = StringField()
    loc = StringField()
    
    nick_name = StringField()
    fensi = StringField()
    guan_zhu = StringField()
    friend = StringField()
    

# 插入原始的数据
def insert_original():
    with open('test/test_nolabels.txt') as fr:
        for one_line in fr.readlines():
            one_weibo = WeiboResult(one_line[:-2],'','','','','','','')
            one_weibo.save()
    pass

# 插入昵称
def insert_nickname():
    with open('test/test_info.txt') as fr:
        for one_line in fr.readlines():
            one_line_split = one_line[:-1].split('||')
            uid = one_line_split[0]
            nickname = one_line_split[1] if one_line_split[1] != 'None' else ""
            
            if nickname != '':
                one_user = WeiboResult.objects(uid = uid).first()
                one_user.update(set__nick_name = nickname) 
    
    pass


if __name__ == '__main__':
#     insert_original()
    insert_nickname()
    pass