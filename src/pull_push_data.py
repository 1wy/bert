from sys import argv
from sqlalchemy import create_engine
from pymysql import connect
import pandas as pd

def pull_data():
	def update_useful(df):
		conn = connect(host='10.24.224.249', port=3306, database='webdata', user='wy', password=',.,.,l',charset='utf8')
		cur = conn.cursor()
		for url, score in zip(df['URL'], df['scores']):
			sql = "update EastMoney set SCORE=%f where URL=\'%s\'" % (score, url)
			cur.execute(sql)
		cur.close()
		conn.close()

	mysql_wind = create_engine('mysql://fineng:123456@10.24.224.249/wind?charset=utf8')
	code_name = pd.read_sql('select S_INFO_WINDCODE, S_INFO_NAME from MyAShareDescription',mysql_wind).set_index('S_INFO_WINDCODE')

	mysql_webdata = create_engine('mysql://wy:,.,.,l@10.24.224.249/webdata?charset=utf8')
	# data = pd.read_sql('select S_INFO_WINDCODE, TITLE, URL from EastMoney where (USEFUL=1) and (SCORE is NULL) limit %d' % 2048,engine)
	data = pd.read_sql('select S_INFO_WINDCODE, TITLE, URL from EastMoney2 where (USEFUL=1) limit %d' % 128, mysql_webdata)
	# data = data.merge(code_name[['S_INFO_WINDCODE']])

	data['TITLE'] = [s.replace(code_name.loc[c].values[0], '').replace(c, '') for c, s in zip(data['S_INFO_WINDCODE'], data['TITLE'])]
	data.to_csv('input.csv')

def push_data():
	#
	# df_results = pd.DataFrame({'SCORE': scores, 'URL': self.data_URL})
	# df = pd.DataFrame({'SCORE': scores, 'TITLE': self.content})
	# print(df)
	df = pd.read_csv('../output/output.csv')
	conn = connect(host='10.24.224.249', port=3306, database='webdata', user='wy', password=',.,.,l',charset='utf8')
	cur = conn.cursor()
	for url, score in zip(df['URL'], df['SCORE']):
		sql = "update EastMoney2 set SCORE=%f where URL=\'%s\'" % (score, url)
		cur.execute(sql)
	cur.close()
	conn.close()

if __name__ == '__main__':
	if argv[1] == 'pull':
		pull_data()
	elif argv[1] == 'push':
		push_data()
	else:
		raise ValueError('please input right operation: pull or push')
