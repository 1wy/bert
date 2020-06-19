
from copy import deepcopy
from sqlalchemy import create_engine
from pymysql import connect
import pandas as pd
import numpy as np
import datetime
import os

def run():
	def update_useful(df_nouse):
		if len(df_nouse) == 0:
			return
		conn = connect(host='10.24.224.249', port=3306, database='wind', user='wy', password=',.,.,l',charset='utf8')
		cur = conn.cursor()
		for ID in df_nouse.index:
			sql = "update FinancialNews set USEFUL=0 where ID=\'%s\'" % (ID)
			cur.execute(sql)
		cur.close()
		conn.close()

	def insert_score():
		def add_tradedate(df):
			min_date = datetime.datetime.strptime(df['DATE'].min(), "%Y%m%d")
			max_date = datetime.datetime.strptime(df['DATE'].max(), "%Y%m%d")
			date_begin = (min_date + datetime.timedelta(days=-30)).strftime('%Y%m%d')
			date_end = (max_date + datetime.timedelta(days=30)).strftime('%Y%m%d')
			mysql_conn = create_engine('mysql://wy:,.,.,l@10.24.224.249/wind?charset=utf8')
			trade_days = pd.read_sql('select TRADE_DAYS from MyAShareCalendar where S_INFO_EXCHMARKET="SSE" order by TRADE_DAYS',mysql_conn).rename(columns={'TRADE_DAYS': 'TRADE_DT'})
			trade_days['DATE'] = trade_days['TRADE_DT']
			all_date = pd.DataFrame({'DATE': [str(d)[:10].replace('-', '') for d in pd.date_range(date_begin, date_end)]})
			all_date = all_date.merge(trade_days[['DATE', 'TRADE_DT']], how='left')
			all_date['TRADE_DT'] = all_date['TRADE_DT'].bfill()
			all_date['NEXTDATE'] = all_date['DATE'].shift(-1)
			# all_date = all_date.set_index('date')

			df = df.merge(all_date[['DATE', 'NEXTDATE']], how='left')
			df.loc[df['TIME'] > '15:00:00', 'DATE'] = np.nan
			df['DATE'] = df['DATE'].fillna(df['NEXTDATE'])
			df = df.merge(all_date[['DATE','TRADE_DT']],how='left')
			return df

		df = pd.read_csv('../output/output.csv',index_col=0)
		df_t = pd.read_csv('../output/time.csv',dtype={'DATE':str},index_col=0)
		df = pd.concat([df,df_t],axis=1)
		df = add_tradedate(df)
		conn = connect(host='10.24.224.249', port=3306, database='wind', user='wy', password=',.,.,l',charset='utf8')

		cur = conn.cursor()
		for i in range(len(df)):
			sql = "update FinancialNews set `SCORE`=%f,`TRADE_DT`=\'%s\' where ID=\'%s\'" % (df.iloc[i]['SCORE'], df.iloc[i]['TRADE_DT'],df.index[i])
			cur.execute(sql)
		cur.close()
		conn.close()

	def clean_output():
		if os.path.exists('../output/output.csv'):
			os.remove('../output/output.csv')
		if os.path.exists('../output/time.csv'):
			os.remove('../output/time.csv')
		if os.path.exists('input.csv'):
			os.remove('input.csv')

	pull_size = 2048
	mysql_wind = create_engine('mysql://fineng:123456@10.24.224.249/wind?charset=utf8')
	code_name = pd.read_sql('select S_INFO_WINDCODE, S_INFO_NAME from MyAShareDescription',mysql_wind)
	code_name['Code'] = code_name['S_INFO_WINDCODE']
	code_name = code_name.set_index('Code')

	data = pd.read_sql('select ID, DATE, TIME, S_INFO_WINDCODE, TITLE from FinancialNews where (USEFUL=1) and (SCORE is NULL) limit %d' % pull_size,mysql_wind)
	# data = pd.read_sql('select ID, S_INFO_WINDCODE, TITLE from FinancialNews where (USEFUL=1) limit %d' % pull_size, mysql_wind)
	# os.system('aipaas login -u wxw -p wy123456')
	cnt = 0
	while len(data)>0:
		data['flag'] = 0
		data_copy = deepcopy(data).set_index('ID')
		data = data.merge(code_name[['S_INFO_WINDCODE']]).set_index('ID')
		data_copy.loc[data.index,'flag'] = 1
		data_nouse = data_copy[data_copy['flag']==0]
		# update_useful(data_nouse)
		clean_output()

		data['TITLE'] = [s.replace(code_name.loc[c].values[0], '').replace(c, '') for c, s in zip(data['S_INFO_WINDCODE'], data['TITLE'])]
		data = data.drop(['S_INFO_WINDCODE','flag'], axis=1)
		data[['TITLE']].to_csv('input.csv')
		data[['DATE','TIME']].to_csv('../output/time.csv')
		# os.system('aipaas airun "./run_cloud.sh" --gpu 1 -u wxw -p wy123456 -w ./ -o ../output')

		output = deepcopy(data)
		output['SCORE'] = 0.5
		output[['SCORE']].to_csv('../output/output.csv')

		insert_score()
		# data = pd.read_sql('select ID, S_INFO_WINDCODE, TITLE from FinancialNews where (USEFUL=1) limit %d' % pull_size,mysql_wind)
		# data = pd.read_sql('select ID, S_INFO_WINDCODE, TITLE from FinancialNews where (USEFUL=1) and (SCORE is NULL) limit %d' % pull_size,mysql_wind)

		print('finishing new batch')

if __name__ == '__main__':
	run()