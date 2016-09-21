# coding:utf8
'''
Created on 2016年7月24日

@author: Xuehj
'''
import codecs
from tutils_about_weibo import tranfiorm_age, process_one_weibo_return_loclist, \
    tran_loc_to_request, determine_one_word_is_location
from utils_about_weibo_3 import read_status, read_lable, read_links
from utils_about_weibo_2 import read_train_weibo_status, \
    filter_source_and_content_list, read_train_weibo_status_for_age
import csv
import sys
from construct_feature_for_age_predict import train_and_predict_age

reload(sys)  
sys.setdefaultencoding('utf8') 

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
                    answer_shet[uid]['age'] = '1990+'
                    
                if one in defnateli_fmale and uid in answer_shet:
                    answer_shet[uid]['sex'] = 'f'
                    answer_shet[uid]['age'] = '1990+'
            
            # 昵称中 包好 19 年代
            if u'19' in nickname:
                try:
                    age = int(nickname[nickname.find(u'19'):nickname.find(u'19') + 4])
                    answer_shet[uid]['age'] = tranfiorm_age(age)
                except ValueError:
                    pass                      
    pass



# 第二步 根据微博中出现的地名信息，填写一部分微博
def count_on_location(answer_shet):
    
    uid_map_loclist = {}
    with codecs.open('test/test_status.txt', 'r', 'utf8') as fr:
        for one_line in fr.readlines():
            one_line_split = one_line[:-2].split(',')
            if len(one_line_split) < 5:
                continue
            uid = one_line_split[0]
            source = one_line_split[3]
            
            content = one_line_split[5]
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
                answer_shet[uid]['loc'] = pick_location(uid_map_loclist[uid])
    pass

# 从一个list中选出出现次数大于半数的地名
def pick_location(loc_list):
#     max_count = max([loc_list.count(w) for w in set(loc_list)])
    for loc in loc_list:
        if loc_list.count(loc) >= len(loc_list) / 2:
            return loc
    return loc_list[0]





# 第3步 根据微博 男女的用词习惯，填写一部分微博的 sex
def count_on_source_and_content(answer_shet, m_map_word_count_content, f_map_word_count_content, m_map_word_count_source, f_map_word_count_source):
    test_status = read_status('test/test_status.txt')
    for uid in answer_shet:
        if uid not in test_status or answer_shet[uid]['sex'] != '':
            continue
        male_pro_bility_source = 0.0
        fmal_pro_bility_source = 0.0
        m_pro_bility_count_source = 0.0
        f_pro_bility_count_source = 0.0
        
        male_pro_bility_content = 0.0
        fmal_pro_bility_content = 0.0
        m_pro_bility_count_content = 0.0
        f_pro_bility_count_content = 0.0
        
        for one_weibo in test_status[uid]:
            source = one_weibo[2]
            content = one_weibo[4]
            
            for one_word in filter_source_and_content_list(source.split(' ')):
                
                if len(one_word) < 2:
                    continue
                
                this_male_pro = float(m_map_word_count_source.get(one_word, 0.0)) / (m_map_word_count_source.get(one_word, 0.0) + f_map_word_count_source.get(one_word, 0.0) + 1.0)
                this_female_pro = float(f_map_word_count_source.get(one_word, 0.0)) / (m_map_word_count_source.get(one_word, 0.0) + f_map_word_count_source.get(one_word, 0.0) + 1.0)
                if this_male_pro > 0.0:
                    male_pro_bility_source += this_male_pro
                    m_pro_bility_count_source += 1
                if this_female_pro > 0.0:
                    fmal_pro_bility_source += this_female_pro
                    f_pro_bility_count_source += 1
                
            for one_word in filter_source_and_content_list(content.split(' ')):
                
                if len(one_word) < 2:
                    continue
                
                this_male_pro = float(m_map_word_count_content.get(one_word, 0.0)) / (m_map_word_count_content.get(one_word, 0.0) + f_map_word_count_content.get(one_word, 0.0) + 1.0)
                this_female_pro = float(f_map_word_count_content.get(one_word, 0.0)) / (m_map_word_count_content.get(one_word, 0.0) + f_map_word_count_content.get(one_word, 0.0) + 1.0)
                
                if this_male_pro > 0.0:
                    male_pro_bility_content += this_male_pro
                    m_pro_bility_count_content += 1
                if this_female_pro > 0.0:
                    fmal_pro_bility_content += this_female_pro
                    f_pro_bility_count_content += 1
        
        male_pro_bility_source /= m_pro_bility_count_source
        fmal_pro_bility_source /= f_pro_bility_count_source
        
        male_pro_bility_content /= m_pro_bility_count_content
        fmal_pro_bility_content /= f_pro_bility_count_content
        
        if male_pro_bility_source > fmal_pro_bility_source and male_pro_bility_content > fmal_pro_bility_content:
            answer_shet[uid]['sex'] = 'm'
            continue
        if male_pro_bility_source < fmal_pro_bility_source and male_pro_bility_content < fmal_pro_bility_content:
            answer_shet[uid]['sex'] = 'f'
            continue
        
        if male_pro_bility_content > fmal_pro_bility_content:
            answer_shet[uid]['sex'] = 'm'
            continue
        else:
            answer_shet[uid]['sex'] = 'f'
            continue
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


# 第 5 步，假设各年龄段的用词是有区别的，这里对于用词
def count_on_word_in_weibo_for_age(answer_shet, before_79_map_word_count_source, in_80_to_89__map_word_count_source, past_90__map_word_count_source, \
                                    before_79_map_word_count_content, in_80_to_89__map_word_count_content, past_90__map_word_count_content):
    test_status = read_status('test/test_status.txt')
    for uid in answer_shet:
        if uid not in test_status or answer_shet[uid]['age'] != '':
            continue
        before_79_pro_bility = 0.0
        in_80_to_89_pro_bility = 0.0
        past_90_pro_bility = 0.0
        
        before_79_count = 0.0
        in_80_to_89_count = 0.0
        past_90_count = 0.0
        
        all_word = 0.0
        
        for one_weibo in test_status[uid]:
            source = one_weibo[2]
            content = one_weibo[4]
            
            for one_word in filter_source_and_content_list(source.split(' ')):
                if len(one_word) < 2:
                    continue
                
                all_word += 1.0
                this_before_79_pro_bility = float(before_79_map_word_count_source.get(one_word, 0.0)) / (before_79_map_word_count_source.get(one_word, 1.0) + in_80_to_89__map_word_count_source.get(one_word, 1) + past_90__map_word_count_source.get(one_word, 1))
                this_in_80_to_89_pro_bility = float(in_80_to_89__map_word_count_source.get(one_word, 0.0)) / (before_79_map_word_count_source.get(one_word, 1.0) + in_80_to_89__map_word_count_source.get(one_word, 1) + past_90__map_word_count_source.get(one_word, 1))
                this_past_90_pro_bility = float(past_90__map_word_count_source.get(one_word, 0.0)) / (before_79_map_word_count_source.get(one_word, 1.0) + in_80_to_89__map_word_count_source.get(one_word, 1) + past_90__map_word_count_source.get(one_word, 1))
                
#                 print '  jj ',this_before_79_pro_bility,this_in_80_to_89_pro_bility,this_past_90_pro_bility,len(before_79_map_word_count_source),one_word,one_word in past_90__map_word_count_source,past_90__map_word_count_source.get(one_word, 0.0)
                if this_before_79_pro_bility > 0.0:
                    before_79_count += 1
                    before_79_pro_bility += this_before_79_pro_bility
                if this_in_80_to_89_pro_bility > 0.0:
                    in_80_to_89_count += 1
                    in_80_to_89_pro_bility += this_in_80_to_89_pro_bility
                if this_past_90_pro_bility > 0.0:
                    past_90_count += 1
                    past_90_pro_bility += this_past_90_pro_bility
                pass
            for one_word in filter_source_and_content_list(content.split(' ')):
                if len(one_word) < 2:
                    continue
                
                all_word += 1.0
                this_before_79_pro_bility = float(before_79_map_word_count_content.get(one_word, 0.0)) / (before_79_map_word_count_content.get(one_word, 1.0) + in_80_to_89__map_word_count_content.get(one_word, 1) + past_90__map_word_count_content.get(one_word, 1))
                this_in_80_to_89_pro_bility = float(in_80_to_89__map_word_count_content.get(one_word, 0.0)) / (before_79_map_word_count_content.get(one_word, 1.0) + in_80_to_89__map_word_count_content.get(one_word, 1) + past_90__map_word_count_content.get(one_word, 1))
                this_past_90_pro_bility = float(past_90__map_word_count_content.get(one_word, 0.0)) / (before_79_map_word_count_content.get(one_word, 1.0) + in_80_to_89__map_word_count_content.get(one_word, 1) + past_90__map_word_count_content.get(one_word, 1))
                
                
#                 print '  222 jj ',this_before_79_pro_bility,this_in_80_to_89_pro_bility,this_past_90_pro_bility,len(before_79_map_word_count_content)
                
                if this_before_79_pro_bility > 0.0:
                    before_79_count += 1
                    before_79_pro_bility += this_before_79_pro_bility
                if this_in_80_to_89_pro_bility > 0.0:
                    in_80_to_89_count += 1
                    in_80_to_89_pro_bility += this_in_80_to_89_pro_bility
                if this_past_90_pro_bility > 0.0:
                    past_90_count += 1
                    past_90_pro_bility += this_past_90_pro_bility
                pass
        
        if before_79_count > 0.0:
            before_79_pro_bility /= all_word
        if in_80_to_89_count > 0.0:
            in_80_to_89_pro_bility /= all_word
        if past_90_count > 0.0:
            past_90_pro_bility /= all_word
        
        print before_79_pro_bility, in_80_to_89_pro_bility, past_90_pro_bility
        
        max_pro = max([before_79_pro_bility, in_80_to_89_pro_bility, past_90_pro_bility])
        min_pro = min([before_79_pro_bility, in_80_to_89_pro_bility, past_90_pro_bility])
        
        # 当相差不大的时候，没有意义
#         if max_pro-min_pro<0.1:
#             continue
        
        if before_79_pro_bility == max_pro:
            answer_shet[uid]['age'] = u'-1979'
        if in_80_to_89_pro_bility == max_pro:
            answer_shet[uid]['age'] = u"1980-1989"
        if past_90_pro_bility == max_pro:
            answer_shet[uid]['age'] = u'1990+'
    pass



def count_on_predict(answer_shet):
    pre_result = train_and_predict_age()
    
    for uid in answer_shet:
        if answer_shet[uid]['age'] == '':
            answer_shet[uid]['age'] = pre_result.get(uid, '')
    
    
    pass

##########################################################################################################################
##########################################################################################################################
##########################################################################################################################

# 在答题卡还有控值的时候，随机猜测这个值
def guess_missing_data(answer_shet):
    for uid in answer_shet:
        if answer_shet[uid]['age'] == '':
            answer_shet[uid]['age'] = u"1980-1989"
        
        if answer_shet[uid]['loc'] == '':
            answer_shet[uid]['loc'] = u'华东'
        
        if answer_shet[uid]['sex'] == '':
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
                    print uid, 'true: ', tran_loc_to_request(loc), loc, 'false: ', answer_shet[uid]['loc']
                    pass
            if answer_shet[uid]['age'] != '':
                age_yitian += 1
                
                try:
                    if tranfiorm_age(int(age)) == answer_shet[uid]['age']:
                        age_right += 1
                    else:
                        print 'true: ', tranfiorm_age(int(age)), 'false:', answer_shet[uid]['age']
                except ValueError, UnicodeEncodeError:
                    # 转换 int 出错
                    pass
            
    
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
    
#     print '2, 根据 nickname 的男女倾向 猜测 sex 和 age'
#     count_on_nickname(answer_shet)
#       
#     print '3, 根据 weibo 中 地名 的出现频率 猜测 loc'
#     count_on_location(answer_shet)
#      
#     print '4, 根据 weibo 用词 猜测 sex'
    label_map = read_lable() 
#     weibo_map = read_status()
#     m_map_word_count_content, f_map_word_count_content, m_map_word_count_source, f_map_word_count_source = read_train_weibo_status(label_map, weibo_map)
#     count_on_source_and_content(answer_shet, m_map_word_count_content, f_map_word_count_content, m_map_word_count_source, f_map_word_count_source)
      
    print '5, 根据 粉丝 年龄  猜测 age'
    count_on_links(answer_shet, label_map)
     
     
    #  这种方法效果很差，比随机猜测都差 
#     print '6, 根据 用词 来 猜测 age'
#     before_79_map_word_count_source, in_80_to_89__map_word_count_source, past_90__map_word_count_source, before_79_map_word_count_content, in_80_to_89__map_word_count_content, past_90__map_word_count_content = read_train_weibo_status_for_age(label_map, weibo_map)
#     count_on_word_in_weibo_for_age(answer_shet, before_79_map_word_count_source, in_80_to_89__map_word_count_source, past_90__map_word_count_source, \
#                                     before_79_map_word_count_content, in_80_to_89__map_word_count_content, past_90__map_word_count_content)

#     print '7, 根据 特征，预测age'
#     count_on_predict(answer_shet)

#     print '在答题卡还有控值的时候，随机猜测这个值'
#     guess_missing_data(answer_shet)
    
    print 'final, 输出结果'
    write_down(answer_shet, 'temp.csv')
    read_crawl_resut_compare(answer_shet)
    pass
