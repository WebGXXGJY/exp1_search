# encoding = utf-8
import csv
import json
import re

import jieba

stop_word_path = "百度停用词表.txt"
with open(stop_word_path, 'r', encoding='UTF-8') as f:
    s = f.read()
    stop_word_list = s.split('\n')


def read_text(path):
    doc_id, doc_url, doc_title, content = [], [], [], []
    with open(path, 'r', encoding='UTF-8') as f:
        reader = csv.reader(f)
        for r in reader:
            doc_id.append(r[0])
            doc_url.append(r[1])
            doc_title.append(r[2])
            content.append(r[3])
    return doc_id, doc_url, doc_title, content


def word_seg(content):
    l = jieba.lcut_for_search(content)
    result = []
    for term in l:
        if term not in stop_word_list and re.match(r'[+.!/_,$%^*()?;；:-【】\"\'\\ ]+|[+—！，;:。？、~@#￥%…&*（）]+', term)\
                is None:
            result.append(term)
    return result


def write_dict(d, string, target, id):
    words = word_seg(string)
    for word in words:
        if word not in d.keys():
            d[target][word] = {id: 1}
        elif id not in d[word].keys():
            d[target][word][id] = 1
        else:
            d[target][word][id] += 1


def dict_gen(path):
    doc_id, doc_url, doc_title, doc_content = read_text(path)
    d = {'title': {}, 'content': {}}
    for i, content in enumerate(doc_content):
        write_dict(d, content, 'content', doc_id[i])
        write_dict(d, doc_title[i], 'title', doc_id[i])
    str_json = json.dump(d)
    with open("'" + path+"'分词.json", 'w', encoding='UTF-8') as f:
        f.write(str_json)


def dict_get(path):
    d = json.load(path)
    return d



