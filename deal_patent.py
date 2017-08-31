#coding=utf-8
'''
分析专利数据：
	专利数据寿命
	同族专利数据排名
	单篇同族专利被引数排名
'''
import pymongo,json,xlwt
client = pymongo.MongoClient('mongodb://127.0.0.1')
collection = client['raven_dev']

excel = xlwt.Workbook()
table1 = excel.add_sheet(u'同族专利数量排名')


def to_china(dictt):
	return json.dumps(dictt, encoding="UTF-8", ensure_ascii=False)

def family_rank():
	pipeline = [
		# {
		# 	'$group':{
		# 		"_id":{
		# 			u'同族专利数量':u'$同族专利数量'
		# 		},
		# 		'count':{
		# 			'$sum':1
		# 		}
		# 	}
		# },
		{
			'$project':{
				u'同族专利数量':1,
				u'公开(公告)号':1,
				'_id':0
			}
		},
		{
			'$sort':{
				u'同族专利数量':-1
			},
		},
		{
			"$limit":20000
		}
	]
	data = collection['Patentt'].aggregate(pipeline)
	print to_china(data)
	if data['ok'] == 1:
		for index,i in enumerate(data['result']):
			table1.write(index,0,i[u'公开(公告)号'])
			table1.write(index,1,i[u'同族专利数量'])
		excel.save('test.xls')

if __name__ == '__main__':
	family_rank()