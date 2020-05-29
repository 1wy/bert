
from copy import deepcopy
from sqlalchemy import create_engine
from pymysql import connect
import pandas as pd
import os

def run():
	def update_useful(df_nouse):
		if len(df_nouse) == 0:
			return
		conn = connect(host='10.24.224.249', port=3306, database='wind', user='wy', password=',.,.,l',charset='utf8')
		cur = conn.cursor()
		for ID in df_nouse.index:
			sql = "update FinancialNews2 set USEFUL=0 where ID=\'%s\'" % (ID)
			cur.execute(sql)
		cur.close()
		conn.close()

	def insert_score():
		df = pd.read_csv('../output/output.csv')
		conn = connect(host='10.24.224.249', port=3306, database='wind', user='wy', password=',.,.,l',charset='utf8')
		cur = conn.cursor()
		for ID, score in zip(df['ID'], df['SCORE']):
			sql = "update FinancialNews set SCORE=%f where ID=\'%s\'" % (score, ID)
			cur.execute(sql)
		cur.close()
		conn.close()

	def clean_output():
		if os.path.exists('../output/output.csv'):
			os.remove('../output/output.csv')

	pull_size = 204800
	mysql_wind = create_engine('mysql://fineng:123456@10.24.224.249/wind?charset=utf8')
	code_name = pd.read_sql('select S_INFO_WINDCODE, S_INFO_NAME from MyAShareDescription',mysql_wind)
	code_name['Code'] = code_name['S_INFO_WINDCODE']
	code_name = code_name.set_index('Code')

	data = pd.read_sql('select ID, S_INFO_WINDCODE, TITLE from FinancialNews where (USEFUL=1) and (SCORE is NULL) limit %d' % pull_size,mysql_wind)
	# data = pd.read_sql('select ID, S_INFO_WINDCODE, TITLE from FinancialNews2 where (USEFUL=1) limit %d' % pull_size, mysql_wind)
	# os.system('aipaas login -u wxw -p wy123456')
	cnt = 0
	while len(data)>0:
		data['flag'] = 0
		data_copy = deepcopy(data).set_index('ID')
		data = data.merge(code_name[['S_INFO_WINDCODE']]).set_index('ID')
		data_copy.loc[data.index,'flag'] = 1
		data_nouse = data_copy[data_copy['flag']==0]
		update_useful(data_nouse)
		clean_output()

		data['TITLE'] = [s.replace(code_name.loc[c].values[0], '').replace(c, '') for c, s in zip(data['S_INFO_WINDCODE'], data['TITLE'])]
		data = data.drop(['S_INFO_WINDCODE','flag'], axis=1)
		data.to_csv('input.csv')
		os.system('aipaas airun "./run_cloud.sh" --gpu 1 -u wxw -p wy123456 -w ./ -o ../output')
		insert_score()
		# data = pd.read_sql('select ID, S_INFO_WINDCODE, TITLE from FinancialNews2 where (USEFUL=1) limit %d' % pull_size,mysql_wind)
		data = pd.read_sql('select ID, S_INFO_WINDCODE, TITLE from FinancialNews where (USEFUL=1) and (SCORE is NULL) limit %d' % pull_size,mysql_wind)

		print('finishing new batch')

if __name__ == '__main__':
	run()