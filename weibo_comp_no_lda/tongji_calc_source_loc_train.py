# coding:utf8

'''
Created on 2016年8月6日

@author: Xuehj
'''
from utils_about_weibo_3 import read_lable, read_status, read_links
from tutils_about_weibo import process_one_weibo_return_loclist, tranfiorm_age



#  source 和 loc 的关系
def tongji_source_loc(label_map, weibo_map):
    
    source_miss = {}
    source_right = {}
    for uid in weibo_map:
        if uid not in label_map:
            continue
        
        loc = label_map[uid]['loc']
        weibo_list = weibo_map[uid]
#         print loc
        
        
        for one_weibo in weibo_list:
            source = one_weibo[2]
            content = one_weibo[4]
            
            loc_list = process_one_weibo_return_loclist(content)
            if len(set(loc_list))==1:
                if loc_list[0] != loc:
                    source_miss[source]=source_miss.get(source,0)+1
                else:
                    source_right[source]=source_right.get(source,0)+1
    
    jiao_ji = set(source_miss.keys()) & set(source_right.keys())
    source_precision = {}
    for ke in jiao_ji:
        if source_right[ke]>10 and source_miss[ke]>5:
            source_precision[ke] = float(source_right[ke])/(source_right[ke]+source_miss[ke])
    
    precision_items = sorted(source_precision.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
     
    for ke,va in precision_items[-40:]:
        print ke,va,source_right[ke],source_miss[ke]
        
    return source_precision



def age_fensi(label_map,links_map):
    
    count = {}
    linke_count = {}
    
    
    for uid in links_map:
        if uid not in label_map:
            continue
        
        age = label_map[uid]['age']
        
        tran_age = tranfiorm_age(int(age))
        len_links = len(links_map[uid])  
        
        linke_count[tran_age] = linke_count.get(tran_age,0.0)+len_links
        count[tran_age] = count.get(tran_age,0.0)+1.0 
    
    print count
    print linke_count
    pass


if __name__ == '__main__':
    
    age_fensi(read_lable(),read_links())
    
#     tongji_source_loc(read_lable(), read_status())
    pass