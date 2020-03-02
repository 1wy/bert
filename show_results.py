import pandas as pd

dir_text = 'finnews/CloseRet_t-1_t+1/'
dir_output = 'finnews/CloseRet_t-1_t+1/output/'
pred = pd.read_csv(dir_output+'test_results.tsv',header=None,sep='\t')
text = pd.read_csv(dir_text+'test.csv',sep='\t',dtype={'label':str})
date_code = pd.read_csv(dir_text+'test_date.csv',sep='\t')
text['prob'] = pred.iloc[:,1].values
text['date'] = date_code['date'].values
text['code'] = date_code['code'].values
text['pred'] = (text['prob']>0.5).astype(int)
text[['date','code','label','pred','prob','x_test']].to_csv(dir_output+'test_results.csv',index=False)
