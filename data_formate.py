# encoding = utf-8
import divide
import pandas as pd
import math

max_len = 11
data_relate = pd.read_csv('./webinfo-信息检索实验数据/查询-文档相关性标签.csv')
doc_ids = pd.read_csv('./webinfo-信息检索实验数据/文档数据集.csv', usecols=['doc_id'])
n = len(doc_ids)
dic = divide.dict_get('文档数据集.csv标题文章分词.txt')
train_data = []


def tf_idf_cal(word, target, id_doc, doc_num):
    if word not in dic[target].keys():
        return 0
    elif id_doc not in dic[target][word].keys():
        return 0
    else:
        tf = dic[target][word][id_doc]
        df = len(dic[target][word])
        tf_idf = (1 + math.log10(tf)) * (math.log10(doc_num / df))
        return tf_idf


qid = 0
query = []
for index, row in data_relate.iterrows():
    if row['query'] not in query:
        qid += 1
        query.append(row['query'])
    term = [row['label'], qid] + [0.0] * max_len * 2 + [0, row['doc_id']]

    q_word = divide.word_seg(row['query'])
    for idx, words in enumerate(q_word):
        ti1 = tf_idf_cal(words, 'title', row['doc_id'], n)
        ti2 = tf_idf_cal(words, 'content', row['doc_id'], n)
        term[idx + 2] = ti1
        term[max_len + idx + 2] = ti2
    term[24] = sum(term[2:24])
    train_data.append(term)
train_data_df = pd.DataFrame(train_data)
train_data_df.to_csv("./data/train_data.csv", index=False)