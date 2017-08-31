#coding=utf-8
import json

# d = {
#         'math.scu.edu.cn':'数学学院',
#         'physics.scu.edu.cn':'物理科学与技术学院',
#         'chem.scu.edu.cn':'化学学院',
#         'life.scu.edu.cn':'生命科学学院',
#         'eie.scu.edu.cn':'电子信息学院',
#         'mse.scu.edu.cn':'材料科学与工程学院',
#         'msec.scu.edu.cn':'制造科学与工程学院',
#         'seei.scu.edu.cn':'电气信息学院',
#         'scu.edu.cn/sw':'计算机学院',
#         'acem.scu.edu.cn':'建筑与环境学院',
#         'cwrh.scu.edu.cn':'水利水电学院'
# }
# l = []
# for i in d:
#         d1 = {'name':d[i],'url':i,'spider':'true','time':'now_time'}
#         l.append(d1)
# print json.dumps(l, encoding='utf-8',ensure_ascii=False)

from datetime import datetime
    # def close_spider(self,spider):
now_time = datetime.now()

College1 = {
    'math.scu.edu.cn': '数学学院',
    'physics.scu.edu.cn': '物理科学与技术学院',
    'chem.scu.edu.cn': '化学学院',
    'life.scu.edu.cn': '生命科学学院',
    'eie.scu.edu.cn': '电子信息学院',
    'mse.scu.edu.cn': '材料科学与工程学院',
    'msec.scu.edu.cn': '制造科学与工程学院',
    'seei.scu.edu.cn': '电气信息学院',
    'scu.edu.cn/sw': '计算机学院',
    'acem.scu.edu.cn': '建筑与环境学院',
    'cwrh.scu.edu.cn': '水利水电学院'
}
College2 = {
    'ce.scu.edu.cn': '化学工程学院',
    'qfsp.scu.edu.cn': '轻纺与食品学院',
    'cpse.scu.edu.cn': '高分子科学与工程学院',
    'jcfy.scu.edu.cn': '华西基础医学与法医学院',
    'www.hxkq.org': '华西口腔医学院',
    'www.hxsiyuan.cn': '华西公共卫生学院',
    'pharmacy.scu.edu.cn': '华西药学院',
    'ggglxy.scu.edu.cn': '公共管理学院',
    'ftp429.gotoip55.com/index.html': '体育学院',
    'idmr.scu.edu.cn': '灾后重建与管理学院',
    'saa.scu.edu.cn': '空天科学与工程学院',
    'scupi.scu.edu.cn': '匹兹堡学院',
    'sis.scu.edu.cn': '国际关系学院',
    'ccs.scu.edu.cn': '网络空间安全学院'
}
for col in College1:
    d = {
        'uname':'四川大学',
        'cname':College1[col],
        'time':now_time,
        'url':col,
        'spider':'true'
    }
    # self.collection1.insert(d)
for col in College2:
    d = {
        'uname': '四川大学',
        'cname': College2[col],
        'time': now_time,
        'url': col,
        'spider': 'true'
    }
    # self.collection1.insert(d)
