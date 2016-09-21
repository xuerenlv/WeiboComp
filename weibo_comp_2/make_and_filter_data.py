# coding:utf8
'''
Created on 2016年7月24日

@author: Xuehj
'''
import jieba
import codecs
import os

# 读取停用词
def read_stop_words_li(file_name):
    stop_words_li = []
    with open(file_name, 'r') as fr:
        for one_ine in fr.readlines():
            stop_words_li.append(one_ine[:-1])
    return stop_words_li


# 去除 @ 信息
def remove_at_info(content):
    at_index = content.find('@')
    if at_index == -1 :
        return content
    else:
        new_content = content[:at_index]
        content = content[at_index:]
        
        maohao_index = content.find(':')
        space_index = content.find(' ')
        
        start_index = min(maohao_index, space_index) if maohao_index != -1 and space_index != -1 else max(maohao_index, space_index)
        new_content = new_content + content[start_index + 1 if start_index != -1 else 1:]
        return remove_at_info(new_content)


# 处理一条微博，达不到要求的话返回 ""
def process_oneweibo(weibo_content, stop_words_li):
    
    # 长度较小 没有价值
    if len(weibo_content) < 6 :
        return ""
    
    weibo_content = remove_at_info(weibo_content)
    
    # 长度较小 没有价值
    if len(weibo_content) < 6 :
        return ""
    
    weibo_content.replace('/', '')
    weibo_content.replace('／', '')
    weibo_content.replace(' ', '')
    
    cut_content = ""
    try:
        cut_content = [w for w in jieba.cut(weibo_content) if w not in stop_words_li]
        
    except :
        print "exception"
        return ""
    
    if len(cut_content) < 6:
        return ""
    else:
        return ' '.join(cut_content)


# 读取 微博 分词 写入 以 姓名 命名的文件
def read_file(file_name, result_dir):
    stop_words = read_stop_words_li('stoplist.txt')
    
    with codecs.open(file_name, 'r') as fr:
        for one_line in fr.readlines():
            one_line_split = one_line[:-1].split(",")
            proced_content = process_oneweibo(one_line_split[5], stop_words)
            
            if len(proced_content) != 0:
                with codecs.open(result_dir + "/" + one_line_split[0] + ".txt", 'a', 'utf8') as fw:
                    fw.write(proced_content + "\n")
                    
            
            
            pass
    
    
    pass







if __name__ == '__main__':
    read_file("unlabeled_statuses.txt_5000_tmp.txt", 'user_weibo_result')
    pass
