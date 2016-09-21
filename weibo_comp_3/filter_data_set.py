# coding:utf8
'''
Created on 2016年7月24日

@author: Xuehj
'''
import os



# 读取停用词
def read_stop_words_li(file_name):
    stop_words_li = []
    with open(file_name, 'r') as fr:
        for one_ine in fr.readlines():
            stop_words_li.append(one_ine[:-1])
    return stop_words_li




def read_dir_and_filter(old_dir, new_dir, stop_words_li):
    
    count = 1
    
    for one_file in os.listdir(old_dir):
        print count
            
        with open(new_dir + "/" + one_file, 'w') as fw:
            one_line = ""
            with open(old_dir + "/" + one_file, 'r') as fr:
                for in_one_line in fr.readlines():
                    this_split_line = [w for w in in_one_line[:-1].split(' ') if w not in stop_words_li]
                    if len(this_split_line) < 5:
                        continue
                    one_line += (' ' if len(one_line)!=0 else "")+' '.join(this_split_line)
            fw.write(one_line + "\n")
        count += 1
            
            
        pass
    
    pass


if __name__ == '__main__':
    stop_words_li = read_stop_words_li('stoplist.txt')
    read_dir_and_filter('user_weibo_result', "new___user_weibo_result",stop_words_li)
    pass
