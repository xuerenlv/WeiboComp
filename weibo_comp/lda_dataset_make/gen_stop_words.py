# coding:utf8
'''
Created on 2016年7月22日

@author: Xuehj
'''
import jieba
import codecs


all_word_map_count = {}


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
def process_oneweibo(weibo_content):
    
    # 长度较小 没有价值
    if len(weibo_content) < 4 :
        return ""
    
    weibo_content = remove_at_info(weibo_content)
    
    # 长度较小 没有价值
    if len(weibo_content) < 4 :
        return ""
    
    weibo_content.replace('/','')
    return weibo_content

# 读取文件
def read_file_gen_stopwords(file_name):
    
    with open(file_name, 'r') as fr:
        for one_line in fr.readlines():
            one_line_split = one_line[:-1].split(",")
            proced_content = process_oneweibo(one_line_split[5])
            if len(proced_content) != 0:
                try:
                    for one_word in jieba.cut(proced_content):
                        all_word_map_count[one_word] = all_word_map_count.get(one_word, 0) + 1
                except:
                    print "exception"
                    continue 
                                 

# 将 停用词存到文件中                         
def store_to_file(file_name):
    word_re_index = sorted(all_word_map_count.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    with codecs.open(file_name,'w','utf8') as fw:
        for one_word,count in word_re_index[:300]:
            fw.write(one_word+"\n")
     
    pass

if __name__ == '__main__':
    read_file_gen_stopwords("unlabeled_statuses.txt")
    store_to_file('stopwords_xhjgen_all_unlabled_weibo.txt')
    pass
