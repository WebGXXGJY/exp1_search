import csv
import random
import time
import pyltr


def feature_process(path):
    fp = open(path, 'r')
    csv.field_size_limit(500*1024*1024)
    reader = csv.reader(fp)
    l = []
    for i, r in enumerate(reader):
        if i == 0:
            continue
        r[1] = 'qid:' + r[1]
        for j in range(2, len(r) - 1):
            r[j] = '%d:%s' % (j - 1, r[j])
        r[-1] = '#docid = %s' % r[-1]
        l.append(' '.join(r))
    fp.close()
    s = '\n'.join(l)
    fp = open('test.txt', 'w')
    fp.write(s)


def sample_validation(path):

    with open(path) as fp:
        X, Y, qids, _ = pyltr.data.letor.read_dataset(fp)
    l = []
    for qid in qids:
        if qid not in l:
            l.append(qid)
    random.seed(time.time())
    valid_list = random.sample(l, k=int(len(l) / 6))
    valid = []
    train = []
    with open(path) as fp:
        dataset = fp.read().split('\n')
    for i, row in enumerate(dataset):
        if i >= len(qids):
            break
        if qids[i] in valid_list:
            valid.append(row)
        else:
            train.append(row)
    with open('valid.txt', 'w') as fp_valid:
        fp_valid.write('\n'.join(valid))
    with open('train.txt', 'w') as fp_train:
        fp_train.write('\n'.join(train))


if __name__ == "__main__":
    feature_process('data/result.csv')
    # sample_validation('data/train_data.csv.txt')