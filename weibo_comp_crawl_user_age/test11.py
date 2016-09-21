# -*- coding: utf-8 -*-
'''
Created on 2016年5月2日

@author: nlp
'''
from store_model import UserInfo_store




if __name__ == '__main__':
    
    print len( UserInfo_store.objects( uid_or_uname = str( "2080114694" ) ) )
    pass