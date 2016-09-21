# coding:utf8
'''
Created on 2016年7月24日

@author: Xuehj
'''
import codecs
import csv
import sys

from tutils_about_weibo import tranfiorm_age, process_one_weibo_return_loclist, tran_loc_to_request
from new_idea_1 import gen_model_predict_result
from new_idea_1 import read_predict_result
from utils_about_weibo_3 import read_links, read_lable, read_status

reload(sys)  
sys.setdefaultencoding('utf8') 

# 预测
# age_predict_map,sex_predict_map,loc_predict_map = gen_model_predict_result()
age_predict_map,sex_predict_map,loc_predict_map = read_predict_result()

# 构建答题卡
def read_data_make_answer_shet():
    answer_shet = {}
    with open('test/test_nolabels.txt') as fr:
        for one_line in fr.readlines():
            answer_shet [one_line[:-2]] = {}
            answer_shet [one_line[:-2]]['sex'] = ''
            answer_shet [one_line[:-2]]['age'] = ''
            answer_shet [one_line[:-2]]['loc'] = ''
    
    return answer_shet


# 第一步 根据 昵称 进行 先验猜测
def count_on_nickname(answer_shet):
#     weibo_map_test = read_status(file_name='test/test_status.txt')
#     for uid in weibo_map_test:
#         if uid not in answer_shet:
#             print uid
#             continue
#         content_concated = "".join([ one_con_li[4] for one_con_li in weibo_map_test[uid]])
#         if u"毕业季" in content_concated or u'毕业' in content_concated:
#             answer_shet[uid]['age'] = '1990+'
            
    
    
    defnateli_fmale = [u'花', u'娟', u'女', u'妹', u'菇凉', u'姐', u'夫人', u'靓', u'姐', u'公主', u'贝', u'丫', u'girl']
    defnateli_male = [u'少爷', u'龙', u'爷', u'帅', u'年', u'男', u'血', u'绅士', u'王', u'皇', u'帝', u'书生', u'爸', u'boy']
    
    with codecs.open('test/test_info.txt', 'r', 'utf8') as fr:
        for one_line in fr.readlines():
            one_line_split = one_line[:-1].split('||')
            uid = one_line_split[0]
            nickname = one_line_split[1] if one_line_split[1] != 'None' else ""
            
            for one in nickname:
                if one in defnateli_male and uid in answer_shet :
                    answer_shet[uid]['sex'] = 'm'
#                     answer_shet[uid]['age'] = '1990+'
                    
                if one in defnateli_fmale and uid in answer_shet:
                    answer_shet[uid]['sex'] = 'f'
#                     answer_shet[uid]['age'] = '1990+'
            
            # 昵称中 包好 19 年代
            if u'19' in nickname:
                try:
                    age = int(nickname[nickname.find(u'19'):nickname.find(u'19') + 4])
                    answer_shet[uid]['age'] = tranfiorm_age(age)
                except ValueError:
                    pass                      
    pass




# 第 4 步，根据 粉丝（这个粉丝不可以太 hot） 推测其年龄
def count_on_links(answer_shet, train_lable):
    test_read_links = read_links('test/test_links.txt')
    for uid in answer_shet:
        fensi_age_sum = 0.0
        count_age = 0.0
        
        if uid not in test_read_links or answer_shet[uid]['age'] != '':
            continue
        
        for one_fans in test_read_links[uid]:
            if one_fans in train_lable:
                fensi_age_sum += train_lable[one_fans]['age']
                count_age += 1
        
        if count_age == 0:
            continue
        mean_age = fensi_age_sum / count_age
        answer_shet[uid]['age'] = tranfiorm_age(int(mean_age))
    pass


uid_map_loclist = {}
# 第二步 根据微博中出现的地名信息，填写一部分微博
def count_on_location(answer_shet):
    global uid_map_loclist
    with codecs.open('test/test_status.txt', 'r', 'utf8') as fr:
        for one_line in fr.readlines():
            one_line_split = one_line[:-2].split(',')
            if len(one_line_split) < 5:
                continue
            uid = one_line_split[0]
            source = one_line_split[3]
            
            content = one_line_split[5]
            
#             if u'分享' in source:
#                 continue
            
            
            if uid not in uid_map_loclist:
                uid_map_loclist[uid] = []
            
#             # 来源为： xi
#             if determine_one_word_is_location(source[-2:]):
#                 answer_shet[uid]['loc'] = tran_loc_to_request(source[-2:])
            
#             if u'头条' in source:
#                 continue

            loc_list = process_one_weibo_return_loclist(content)
            
            uid_map_loclist[uid].extend(loc_list)
    
    for uid in uid_map_loclist:
        if len(uid_map_loclist[uid]) == 0:
            continue
        else:
#             print uid,len(uid_map_loclist[uid]),len(set(uid_map_loclist[uid])),' '.join(set(uid_map_loclist[uid])),'---',' '.join(uid_map_loclist[uid])
            if uid in answer_shet and answer_shet[uid]['loc'] == '':
                
#                 if loc_predict_map[uid] in set(uid_map_loclist[uid]):
#                     answer_shet[uid]['loc'] = loc_predict_map[uid]
#                     break
                
#                 if u'2630267160'==uid:
#                     print ' '.join(uid_map_loclist[uid])
                
                answer_shet[uid]['loc'] = pick_location(uid_map_loclist[uid])
    pass

# 从一个list中选出出现次数大于半数的地名
def pick_location(loc_list):
#     print "size: ",len(set(loc_list))
#     max_count = max([loc_list.count(w) for w in set(loc_list)])
    for loc in loc_list:
        if loc_list.count(loc) >= len(loc_list) / 2:
            return loc
    return loc_list[0]



##########################################################################################################################
##########################################################################################################################
##########################################################################################################################

# 在答题卡还有控值的时候，随机猜测这个值
def guess_missing_data(answer_shet):
    for uid in answer_shet:
        if answer_shet[uid]['age'] == '':
            answer_shet[uid]['age'] = '1980-1989'
#             answer_shet[uid]['age'] = age_predict_map[uid]
        
        if answer_shet[uid]['loc'] == '':
            answer_shet[uid]['loc'] = "华东"
#             answer_shet[uid]['loc'] = loc_predict_map[uid]
        
        if answer_shet[uid]['sex'] == '':
            answer_shet[uid]['sex'] = "f"
#             answer_shet[uid]['sex'] = sex_predict_map[uid]
            pass
    pass

# 最后一步，将结果写入答题纸
# uid,age,gender,province
def write_down(answer_shet, result_file_name):
    
    all_count = 0
    in_count = [0, 0, 0]
    with open(result_file_name, 'wb') as csv_file:
        wt = csv.writer(csv_file)
        
        wt.writerow(['uid', 'age', 'gender', 'province'])
        for one_uid in answer_shet:
            all_count += 1
            if answer_shet[one_uid]['age'] != "":
                in_count[0] += 1
            if answer_shet[one_uid]['sex'] != "":
                in_count[1] += 1
            if answer_shet[one_uid]['loc'] != "":
                in_count[2] += 1
#             print one_uid + "," + answer_shet[one_uid]['age'] + "," + answer_shet[one_uid]['sex'] + "," + answer_shet[one_uid]['loc']
#             print answer_shet[one_uid]['loc']
            wt.writerow([one_uid, answer_shet[one_uid]['age'], answer_shet[one_uid]['sex'], answer_shet[one_uid]['loc']])
    print all_count
    print in_count

# 读取最终结果 看看准确率
def read_crawl_resut_compare(answer_shet):
    sex_yitian = 0
    sex_right = 0
    
    loc_yitian = 0
    loc_right = 0
    
    age_yitian = 0
    age_right = 0
    
    with codecs.open('test_nolabels_result.txt', 'r', 'utf8') as fr:
        loc_cando = 0.0
        can_do_uid = []
        for one_line in fr.readlines():
            one_line_sp = one_line[:-1].split(',')
            
            uid = one_line_sp[0]
            sex = one_line_sp[1]
            loc = one_line_sp[2].split(' ')[0]
            age = one_line_sp[4].split('-')[0]
            
        
            if answer_shet[uid]['sex'] != '':
                sex_yitian += 1
                if answer_shet[uid]['sex'] == sex:
                    sex_right += 1 
            if answer_shet[uid]['loc'] != '':
                loc_yitian += 1
                if tran_loc_to_request(loc) == answer_shet[uid]['loc']:
                    loc_right += 1
                else:
                    if tran_loc_to_request(loc) in uid_map_loclist[uid] :
                        can_do_uid.append(uid)
                        loc_cando += 1
                    print uid, 'true: ', tran_loc_to_request(loc), loc, 'false: ', answer_shet[uid]['loc']
                    pass
            if answer_shet[uid]['age'] != '':
                age_yitian += 1
                
                try:
                    if tranfiorm_age(int(age)) == answer_shet[uid]['age']:
                        age_right += 1
                    else:
#                         print answer_shet[uid]['age'].split(" ")
                        print uid,'true: ', tranfiorm_age(int(age)), 'false:', answer_shet[uid]['age']
                except ValueError, UnicodeEncodeError:
                    # 转换 int 出错
                    pass
        print "loc can do :",loc_cando
        print "can do uid :",can_do_uid
    
    print 'sex :', sex_yitian, sex_right
    print 'age :', age_yitian, age_right
    print 'loc :', loc_yitian, loc_right
    print 'current precision :', float(sex_right) / sex_yitian, float(age_right) / age_yitian, float(loc_right) / loc_yitian
    print 'current score :', 0.2 * (float(sex_right) / sex_yitian) + 0.3 * (float(age_right) / age_yitian) + 0.5 * (float(loc_right) / loc_yitian)
    
    print 'global precision :', float(sex_right) / 980, float(age_right) / 980, float(loc_right) / 980
    print 'global score :', 0.2 * (float(sex_right) / 980) + 0.3 * (float(age_right) / 980) + 0.5 * (float(loc_right) / 980)
    pass


if __name__ == '__main__':
    print '1, 构造答题卡'
    answer_shet = read_data_make_answer_shet()
     
    print '2, 根据 nickname 的男女倾向 猜测 sex 和 age'
    count_on_nickname(answer_shet)
           
           
    print '3, 根据 weibo 中 地名 的出现频率 猜测 loc'
    count_on_location(answer_shet)
      
            
    print '4, 根据 粉丝 年龄  猜测 age'
    label_map = read_lable() 
    count_on_links(answer_shet, label_map)
    
   
#     print '在答题卡还有控值的时候，随机猜测这个值'
    guess_missing_data(answer_shet)
    
    print 'final, 输出结果'
    write_down(answer_shet, 'temp.csv')
#     read_crawl_resut_compare(answer_shet)
    pass
