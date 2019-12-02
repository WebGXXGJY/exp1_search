# encoding = utf-8
import jieba
import csv
import re, json

stop_word_path = "百度停用词表.txt"
stop_word_list = []
with open(stop_word_path, 'r', encoding='UTF-8') as f:
    s = f.read()
    stop_word_list = s.split('\n')


def read_text(path):
    doc_id, doc_url, doc_title, content = []
    with open(path, 'r', encoding='UTF-8') as f:
        reader = csv.reader(f)
        for r in reader:
            doc_id.append(r[0])
            doc_url.append(r[1])
            doc_title.append(r[2])
            content.append(r[3])
    return doc_id, doc_url, doc_title, content


def divide(content):
    l = jieba.lcut_for_search(content)
    result = []
    for term in l:
        if term not in stop_word_list and re.match(r'[+.!/_,$%^*()?;；:-【】\"\'\\ ]+|[+—！，;:。？、~@#￥%…&*（）]+', term)\
                is None:
            result.append(term)
    return result


def write_dict(string, target):
    pass


def dict_gen(path):
    doc_id, doc_url, doc_title, doc_content = read_text(path)
    d = {'title': {}, 'content': {}}
    for i, content in enumerate(doc_content):
        words = divide(content)
        for word in words:
            if word not in d.keys():
                d['content'][word] = {doc_id[i]: 1}
            elif doc_id[i] not in d[word].keys():
                d['content'][word][doc_id[i]] = 1
            else:
                d['content'][word][doc_id[i]] += 1
    str_json = json.dump(d)
    with open("'" + path+"'分词.json") as f:
        f.write(str_json)


def dict_get(path):
    d = json.load(path)
    return d



