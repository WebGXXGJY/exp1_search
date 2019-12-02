import divide
import pandas as pd
import math


max_len = 11
data_relate = pd.read_csv('./webinfo-信息检索实验数据/查询-文档相关性标签.csv')
data_doc = pd.red_csv('./webinfo-信息检索实验数据/文档数据集.csv')
n = len(data_doc)
qid = 0
data_relate['qid'] = 0
query = []

dic = divide.dict_get('分词.json')
for index, row in data_relate.iterrows():
    if row['query'] not in query:
        qid += 1
        row['qid'] = qid
        query.append(row['query'])
    string = row['label'] + ' qid:' + str(row['qid'])
    q_word = divide.word_seg(row['query'])
    n_words = len(q_word)

    for idx, words in enumerate(q_word):
        if words not in dic['title'].keys():
            string = string + ' ' + str(idx+1) + ':' + '0'
        else:
            tf = dic['title'][words][row['doc_id']]
            df = len(dic['title'][words])
            tf_idf = (1 + math.log10(tf)) * (math.log10(n/df))
            string = string + ' ' + str(idx+1) + ':' + str(tf_idf)
    if n_words + 1 > max_len-1:
        print("query中的分词过多")
    else:
        for i in range(n_words + 1, max_len):
            string = string + ' ' + str(i+1) + ':' + '0'

    for idx, words in enumerate(q_word):
        if words not in dic['content'].keys():
            string = string + ' ' + str(max_len+idx+1) + ':' + '0'
        else:
            tf = dic['content'][words][row['doc_id']]
            df = len(dic['content'][words])
            tf_idf = (1 + math.log10(tf)) * (math.log10(n/df))
            string = string + ' ' + str(max_len+idx+1) + ':' + str(tf_idf)
    if n_words + 1 > max_len-1:
        print("query中的分词过多")
    else:
        for i in range(n_words + 1, max_len):
            string = string + ' ' + str(max_len+i+1) + ':' + '0'

    with open("train_data.txt", 'a') as data:
        data.write(string + '\n')
