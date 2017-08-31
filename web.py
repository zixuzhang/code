# -*- coding: utf-8 -*-
import json
import re
import sys
import zipfile

import chardet
import gridfs
import tika
from bson.objectid import ObjectId
from flask import Flask, render_template, make_response, request, url_for, redirect, flash, jsonify, abort, session
from flask_bootstrap import Bootstrap
from flask_paginate import Pagination
from flask_script import Manager
from pymongo import MongoClient

tika.initVM()
from app.file_parse.file_parse import File_Parse
from app.filedata_manage.filedata_manage import fulltext_search1, fulltext_search, fulltext_search_all

#解决flash字符编码问题
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

sys.setrecursionlimit(10000)

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
client = MongoClient('localhost',27017)
# db = client.test
db = client.zxjd_database
fs = gridfs.GridFS(db)
categories = db.categories
user = db.user
app.config['SECRET_KEY'] = 'eL7fnDZRL6kEbeAI'

#404错误路由
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

#500错误路由
@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500

#根路由
@app.route('/')
def index():
	page = request.args.get('page', type=int, default=1)
	skip = (page - 1) * 25
	files = fs.find({'filename':{"$ne":''}}).skip(skip).limit(25)
	count = files.count()
	pagination = Pagination(page=page, total=count, css_framework='bootstrap3',per_page=25)
	return render_template('index.html', count=count, files=files,
						   pagination=pagination)

# 导航栏所有项目的路由
@app.route('/project')
def project():

	return

#下载单个文件
@app.route('/<file_id>')
def download(file_id):
	file = fs.get(ObjectId(file_id))
	response = make_response(file.read())
	response.mimetype = 'application/octet-stream'
	filename = file.filename.encode('utf-8')
	response.headers["Content-Disposition"] = "attachment; filename=%s" % filename
	return response

#单文件的删除
@app.route('/<file_id>/delete')
def file_delete(file_id):
	file = fs.get(ObjectId(file_id))
	company_name = file.company_name
	filename = file.filename
	fs.delete(ObjectId(file_id))
	flash(filename + '  已删除')
	return redirect(url_for('company_profile', company_name=company_name))

#查找文件名
@app.route('/search', methods=['GET', 'POST'])
def search():
	if request.method == 'POST':
		search_name = request.form.get('search_name')
		if search_name:
			files = fs.find({'filename': re.compile(search_name)})
			count = files.count()
			return render_template('search.html', files = files, count = count)
	return render_template('search.html')

#全文索引
@app.route('/full_text/search', methods=['GET', 'POST'])
def full_search():
	if request.method == 'POST':
		search_name = request.form.get('search_name')
		if search_name:
			files = fs.find({'text': re.compile(search_name)})
			files_list, count, match_count = fulltext_search(files, search_name)
			return render_template('full_search.html', search_name=search_name, files_list = files_list, count = count,
								   match_count = match_count)
	return render_template('full_search.html')

@app.route('/full_text/search1', methods=['GET', 'POST'])
def full_search1():
	company = fs.find().distinct('company_name')
	if request.method == 'POST':
		search_name = request.form.get('search_name')
		option = request.form.get('option')
		session['search_name'] = search_name
		session['option'] = option
		if search_name:
			if option == u'搜索全部文件':
				files = fs.find({"$or":[{'html': re.compile(search_name)},{'filename': re.compile(search_name)}]})
			elif option == u'搜索文件名':
				files = fs.find({'filename': re.compile(search_name)}).limit(13)
				files_list, count, match_count = fulltext_search_all(files)
				return render_template('full_search1.html', company=company, files_list=files_list,
									   count=count, match_count=match_count, option=session['option'])
			else:
				files = fs.find({"$or":[{'html': re.compile(search_name)},{'filename': re.compile(search_name)}],'company_name':option})
			files_list, count, match_count = fulltext_search1(files, search_name)
			return render_template('full_search1.html', search_name=search_name, company=company, files_list = files_list,
								   count = count, match_count = match_count, option=session['option'])
		else:
			files = fs.find({'filename': {"$ne": ''}})
			files_list, count, match_count = fulltext_search_all(files)
			return render_template('full_search1.html', company=company, files_list=files_list,
								   count=count, match_count=match_count)
	return render_template('full_search1.html', company=company, option='搜索全部文件')



#在当前文件夹下上传文件
@app.route('/file/upload', methods=['GET', 'POST'])
def file_upload():
	if request.method == 'POST':
		files = request.files.getlist("file")
		tag = request.form.get('tag')
		file_md5 = request.form.get('file_md5')
		company_name = tag.split('/')[0]
		for file in files :
			file_copys = fs.find({'md5': file_md5,'tag':tag}).count()
			if file_copys > 0:
				flash(file.filename + '文件已经存在！')
				abort(500)
			else:
				filename = file.filename
				data = file.read()
				fs.put(data, filename=filename, company_name=company_name, tag=tag)
		return render_template('index.html')

#重新上传文件 应用到标签
@app.route('/<file_id>/update',methods=['GET','POST'])
def file_update(file_id):
	file = fs.get(ObjectId(file_id))
	filename2 = file.filename
	company_name1 = file.company_name
	tag = file.tag
	if request.method == 'POST':
		file1 = request.files['file']
		filename1 = file1.filename
		data = file1.read()
		fs.put(data, filename=filename1, company_name=company_name1, tag=tag)
		fs.delete(ObjectId(file_id))
		return redirect(url_for('company_profile', company_name=company_name1))
	return render_template('file_update.html', filename=filename2, file_id=file_id)

#上传压缩包 并把压缩文件的层级结构存储到categories表中，把文件和文件的路径标签存储到GridFS
# @app.route('/upload',methods=['GET','POST'])
# def upload():
# 	if request.method == 'POST':
# 		files = request.files.getlist("file")
# 		file_md5 = request.form.get('file_md5')
# 		for file in files:
# 			file_copys = fs.find({'project':file_md5}).count()
# 			if file_copys > 0:
# 				flash(file.filename + '文件已经存在！')
# 				abort(500)
# 			else:
# 				if zipfile.is_zipfile(file): #判断文件是否是zip类型
# 					zf = zipfile.ZipFile(file, 'r')
# 					for name in zf.namelist():
# 						if isinstance(name, str):
# 							if chardet.detect(name)['encoding'] == 'GB2312':
# 								name1 = unicode(name, 'GBK').encode('utf-8')
# 							else:
# 								name1 = name
# 						else:
# 							name1 = name
# 						c = name1.split('/')#使路径变为列表
# 						if name1[-1] == '/':#根据name判断是否为文件夹，是文件夹的话把目录信息存入cate表
# 							field = c[:-1]
# 							path = c[:-2]
# 							categories.insert_one({'field': field, 'path': path})#把路径信息插入categories表
# 						else:#否则就可以判断出name是文件，然后把文件信息以及标签信息存入GridFS
# 							filename = c[-1]
# 							company_name = c[0]
# 							tag = '/'.join(c[:-1])  # 标签信息包含文件路径不包含文件信息为字符，并用逗号分隔
# 							data = zf.read(name)
# 							# fs.put(data, filename=filename, company_name=company_name, tag=tag, project=file_md5)
# 							#allowed_filetype = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx']
# 							filetype = os.path.splitext(name1)[1]
# 							if filetype == '.pdf':
# 								html_file = pdftostr.pdftohtml(data)
# 								try:
# 									text = pdftostr.pdftostr(data)
# 								except:
# 									fs.put(data, filename=filename, company_name=company_name, tag=tag, project= file_md5, text='',
# 										   html_file=html_file)
# 								else:
# 									#成功把pdf文件转化为text文本，并存入数据库
# 									fs.put(data, filename=filename, company_name=company_name, tag=tag, project= file_md5, text=text,
# 										   html_file=html_file)
# 							elif filetype == '.docx':
# 								docxfile = StringIO.StringIO()
# 								docxfile.write(data)
# 								text = docx2txt.process(docxfile)
# 								#成功把pdf文件转化为text文本，并存入数据库
# 								fs.put(data, filename=filename, company_name=company_name, tag=tag, project= file_md5, text=text)
# 							elif filetype == '.doc':
# 								text = doc2str.doc2str(data)
# 								fs.put(data, filename=filename, company_name=company_name, tag=tag, project=file_md5, text=text)
# 							elif filetype == '.xls':
# 								try:
# 									text = xls2str.xls2str(data)
# 								except:
# 									fs.put(data, filename=filename, company_name=company_name, tag=tag, project=file_md5,
# 											text=text)
# 								else:
# 									fs.put(data, filename=filename, company_name=company_name, tag=tag,
# 										   project=file_md5, text=text)
# 							elif filetype == '.xlsx':
# 								text = xlsx2str.xlsx2str(data)
# 								fs.put(data, filename=filename, company_name=company_name, tag=tag, project=file_md5,
# 									   text=text)
# 							elif filetype == '.ppt':
# 								os.chdir('/home/zxjd/Web/cace')
# 								x_file = open('a.ppt', 'wb')
# 								x_file.write(file.read())
# 								x_file.close()
# 								parsed = parser.from_file('a.ppt')
# 								text = parsed['content']
# 								fs.put(data, filename=filename, company_name=company_name, tag=tag, project=file_md5,
# 									   text=text)
# 							elif filetype == '.pptx':
# 								x_file = open('a.pptx', 'wb')
# 								x_file.write(file.read())
# 								x_file.close()
# 								parsed = parser.from_file('a.pptx')
# 								text = parsed['content']
# 								fs.put(data, filename=filename, company_name=company_name, tag=tag, project=file_md5,
# 									   text=text)
# 							elif filetype == '.txt':
# 								text = data
# 								try:
# 									text = unicode(text, 'GBK').encode('UTF-8')
# 								except:
# 									fs.put(data, filename=filename, company_name=company_name, tag=tag,
# 										   project=file_md5)
# 								else:
# 									fs.put(data, filename=filename, company_name=company_name, tag=tag,
# 										   project=file_md5, text=text)
# 							else:
# 								fs.put(data, filename=filename, company_name=company_name, tag=tag, project= file_md5)
# 		return redirect(url_for('index'))
# 	return render_template('upload.html')

#上传压缩包 并把压缩文件的层级结构存储到categories表中，把文件和文件的路径标签存储到GridFS

@app.route('/upload',methods=['GET','POST'])
def upload():
	if request.method == 'POST':
		files = request.files.getlist("file")
		file_md5 = request.form.get('file_md5')
		for file in files:
			file_copys = fs.find({'project':file_md5}).count()
			if file_copys > 0:
				flash(file.filename + '文件已经存在！')
				abort(500)
			else:
				# 判断文件是否是zip类型
				if zipfile.is_zipfile(file):
					zf = zipfile.ZipFile(file, 'r')
					for name in zf.namelist():
						# 多平台的兼容name1为Unicode
						if isinstance(name, str):
							if chardet.detect(name)['encoding'] == 'GB2312':
								name1 = unicode(name, 'GBK').encode('utf-8')
							else:
								name1 = name
						else:
							name1 = name
						# 使路径变为列表
						c = name1.split('/')
						# 根据name1判断是否为文件夹，是文件夹的话把目录信息存入categories表；
						# 否则就可以判断出name是文件，然后把文件信息以及标签信息存入GridFS
						if name1[-1] == '/':
							field = c[:-1]
							path = c[:-2]
							categories.insert_one({'field': field, 'path': path})
						else:
							filename = c[-1]
							company_name = c[0]
							# 标签信息包含文件路径不包含文件信息为字符，并用斜杠分隔
							tag = '/'.join(c[:-1])
							data = zf.read(name)
							#allowed_filetype = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx']
							file_parse = File_Parse(filename,data)
							text, html, status = file_parse.parse()
							fs.put(data, filename=filename, company_name=company_name, tag=tag, project=file_md5,
									text=text, html=html, status=status)
		return redirect(url_for('index'))
	return render_template('upload.html')

#ajax返回html字段进行预览
@app.route('/query_html')
def query_html():
	file_id = request.args.get('file_id')
	file = fs.get(ObjectId(file_id))
	json_pre = {'html1':file.html,'filename':file.filename}
	return jsonify(json_pre)

#ajax查询各个文件夹下的文件
@app.route('/query')
def query():
	tag = request.args.get('tag', '')
	# tag = "9-成都酉辰科技有限公司/企业项目资料/2-技术附件"
	files = fs.find({'filename': {"$ne": ''}, 'tag': tag})
	count = files.count()
	json_file = {'count':count}
	a=[]
	for file in files:
		a.append({'filename':file.filename,'file_id':str(file._id)})
	json_file['lists'] = a
	return jsonify(json_file)

#ajax获取文件目录信息json
@app.route('/get_json/<company_name>')
def get_json(company_name):
	# 从categories表中生成关于文件结构的json数据，采用递归生成
	def json_tree(field):
		d = {'text': field[-1]}
		d['children'] = [json_tree(x["field"]) for x in categories.find({'path':field })]
		return d
	return json.dumps(json_tree([company_name]))

#公司列表
@app.route('/company')
def company():
	company = fs.find().distinct('company_name')
	return render_template('company.html', company=company)

#公司主页
@app.route('/company/<company_name>')
def company_profile(company_name):
	files = fs.find({'filename': {"$ne": ''},'company_name':company_name})
	count = files.count()
	return render_template('company_profile.html', company_name=company_name, count=count, files=files)

if __name__ == '__main__':
	manager.run()
