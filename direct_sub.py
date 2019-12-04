import pandas as pd

data = pd.read_csv('submission初排.CSV')
submission = pd.DataFrame()

for i in range(470):
    sub = data.iloc[i*100:i*100+20, [1, 2]]
    submission = submission.append(sub, ignore_index=True)

submission.columns = ['query_id', 'doc_id']
submission.to_csv("GKD_submission3.csv", index=False)
