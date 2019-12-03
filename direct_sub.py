import pandas as pd

data = pd.read_csv('result.csv')
submission = pd.DataFrame()

for i in range(470):
    sub = data.iloc[i*100:i*100+20, [1, 24]]
    submission = submission.append(sub, ignore_index=True)

submission.columns = ['query_id', 'doc_id']
submission.to_csv("../exp1_data/submission.csv", index=False)
