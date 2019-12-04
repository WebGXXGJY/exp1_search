# encoding = utf-8
import csv
import json
import re

import jieba

stop_word_path = "百度停用词表.txt"
with open(stop_word_path, 'r', encoding='UTF-8') as fp:
    s = fp.read()
    stop_word_list = s.split('\n')


def read_title_content(path):
    doc_id, doc_url, doc_title, content = [], [], [], []
    with open(path, 'r', encoding='UTF-8') as fp:
        csv.field_size_limit(500 * 1024 * 1024)
        reader = csv.reader(fp)
        for i, r in enumerate(reader):
            if i == 0:
                continue
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
        if word not in d[target].keys():
            d[target][word] = {id: 1}
        elif id not in d[target][word].keys():
            d[target][word][id] = 1
        else:
            d[target][word][id] += 1


def dict_gen_title_content(path):
    doc_id, doc_url, doc_title, doc_content = read_title_content(path)
    d = {'title': {}, 'content': {}}
    for i, content in enumerate(doc_content):
        if i % 1000 == 0:
            print('%d\n' % i)
        write_dict(d, content, 'content', doc_id[i])
        write_dict(d, doc_title[i], 'title', doc_id[i])
    fp = open(path+"标题文章分词.json", 'w', encoding='UTF-8')
    json.dump(d, fp)
    fp.close()


def dict_get(path):
    with open(path, 'r') as fp:
        d = json.load(fp)
    return d


if __name__ == "__main__":
    dict_gen_title_content("测试数据/test_docs.csv")


