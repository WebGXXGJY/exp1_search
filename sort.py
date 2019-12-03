# encoding = utf-8
import divide
import pandas as pd
import math
import numpy as np

max_len = 11
queries = pd.read_csv('./测试数据/test_querys.csv')
doc_ids = pd.read_csv('./webinfo-信息检索实验数据/文档数据集.csv', usecols=['doc_id'])
n = 21485
dic = divide.dict_get('文档数据集.csv标题文章分词.txt')
# result0 = [[] for i in range(26)]
result = pd.DataFrame()


def tf_idf_cal(word, target, id_doc):
    if word not in dic[target].keys():
        return 0
    elif id_doc not in dic[target][word].keys():
        return 0
    else:
        tf = dic[target][word][id_doc]
        df = len(dic[target][word])
        tf_idf = (1 + math.log10(tf)) * (math.log10(n / df))
        return tf_idf


for index, row in queries.iterrows():
    q_word = divide.word_seg(row['query'])
    n_words = len(q_word)
    q_result = []

    for tmp, doc_id in doc_ids.iterrows():
        term = [0, row['query_id']] + [0.0]*max_len*2 + [doc_id['doc_id'], 0]
        for idx, words in enumerate(q_word):
            ti1 = tf_idf_cal(words, 'title', doc_id['doc_id'])
            ti2 = tf_idf_cal(words, 'content', doc_id['doc_id'])
            term[idx + 2] = ti1
            term[max_len + idx + 2] = ti2
        term[25] = sum(term[2:24])
        q_result.append(term)
    q_result1 = pd.DataFrame(q_result)
    q_result0 = q_result1.nlargest(100, 25)
    result.append(q_result0, ignore_index=True)

result.to_csv("result.csv", index=False)


