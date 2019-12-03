import csv
import random,time

def feature_process(path):
    fp = open(path, 'r')
    csv.field_size_limit(500*1024*1024)
    reader = csv.reader(fp)
    l = []
    for i, r in enumerate(reader):
        if i == 0:
            continue
        r[1] = 'qid:' + r[1]
        for j in range(2, len(r) - 2):
            r[j] = '%d:%s' % (j - 1, r[j])
        r[-2] = '#docid = %s' % r[-2]
        r[-1] = 'sum = %s' % r[-1]
        l.append(' '.join(r))
    fp.close()
    s = '\n'.join(l)
    fp = open('test.txt', 'w')
    fp.write(s)


def sample_validation(path):
    fp = open(path, 'r')
    s = fp.read()
    l = s.split('\n')
    random.seed(time.time())
    valid_list = random.sample(range(len(l)), k=int(len(l) / 5))
    valid = []
    train = []
    for i, row in enumerate(l):
        if i in valid_list:
            valid.append(row)
        else:
            train.append(row)
    with open('valid.txt', 'w') as fp_valid:
        fp_valid.write('\n'.join(valid))
    with open('train.txt', 'w') as fp_train:
        fp_train.write('\n'.join(train))


if __name__ == "__main__":
    # feature_process('result.csv')
    sample_validation('train_data.txt')