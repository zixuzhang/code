#coding=utf-8
import json
Spider = {
    "http://www.me.uestc.edu.cn": "微电子与固体电子学院（国家示范性微电子学院）",
    "http://www.life.uestc.edu.cn": "生命科学与技术学院",
    "http://www.iffs.uestc.edu.cn": "基础与前沿研究院",
    "http://www.gla.uestc.edu.cn": "格拉斯哥学院",
    "http://www.math.uestc.edu.cn": "数学科学学院",
    "http://www.iaa.uestc.edu.cn": "航空航天学院",
    "http://www.sre.uestc.edu.cn": "资源与环境学院",
    "http://www.pe.uestc.edu.cn": "物理电子学院",
    "http://www.yingcai.uestc.edu.cn": "英才实验学院",
    "http://www.med.uestc.edu.cn": "医学院",
    "http://www.ncl.uestc.edu.cn": "通信抗干扰技术国家级重点实验室",
    "http://www.energy.uestc.edu.cn": "能源科学与工程学院",
    "http://www.is.uestc.edu.cn": "信息与软件工程学院",
    "http://www.my.uestc.edu.cn": "马克思主义教育学院",
    "http://www.soei.uestc.edu.cn": "光电信息学院",
    "http://www.rw.uestc.edu.cn": "政治与公共管理学院",
    "http://www.ie.uestc.edu.cn": "创新创业学院",
    "http://www.fl.uestc.edu.cn": "外国语学院",
    "http://www.auto.uestc.edu.cn": "自动化工程学院",
    "http://www.ccse.uestc.edu.cn": "计算机科学与工程学院",
    "http://www.scie.uestc.edu.cn": "通信与信息工程学院",
    "http://www.sport.uestc.edu.cn": "体育部（体育场馆管理中心）",
    "http://www.ee.uestc.edu.cn": "电子工程学院",
    "http://www.jxdz.uestc.edu.cn": "机械电子工程学院",
    "http://www.mgmt.uestc.edu.cn": "经济与管理学院"
}

start_urls = []
allowed_domains = []
college = {}

for i in Spider:
	start_urls.append(i)
	u = i.split('www.')[1]
	allowed_domains.append(u)
	college[u] = Spider[i]

print json.dumps(start_urls,encoding='utf-8',ensure_ascii=False)
print json.dumps(allowed_domains,encoding='utf-8',ensure_ascii=False)
print json.dumps(college,encoding='utf-8',ensure_ascii=False)