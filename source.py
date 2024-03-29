# encoding=utf-8
import pyltr


with open('train.txt') as trainfile, \
        open('valid.txt') as valifile, \
        open('test.txt') as evalfile:
    TX, Ty, Tqids, _ = pyltr.data.letor.read_dataset(trainfile)
    VX, Vy, Vqids, _ = pyltr.data.letor.read_dataset(valifile)
    EX, Ey, Eqids, _ = pyltr.data.letor.read_dataset(evalfile)

metric = pyltr.metrics.NDCG(k=10)

# Only needed if you want to perform validation (early stopping & trimming)
monitor = pyltr.models.monitors.ValidationMonitor(
    VX, Vy, Vqids, metric=metric, stop_after=250)

model = pyltr.models.LambdaMART(
    metric=metric,
    n_estimators=1000,
    learning_rate=0.02,
    max_features=0.5,
    query_subsample=0.5,
    max_leaf_nodes=10,
    min_samples_leaf=64,
    verbose=1,
)

print('Start')
model.fit(TX, Ty, Tqids, monitor=monitor)
print('End')
Epred = model.predict(EX)

with open('Epred.txt', 'w') as fp:
    fp.write('\n'.join([str(f) for f in Epred]))

