from flask import Flask, session, redirect, url_for, escape, request, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

app=Flask(__name__)
app.secret_key=b'abbas'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assignment3.db'
db = SQLAlchemy(app)

#收集student信息
def info():
	if 'username' in session:
		sql1 = """
					SELECT *
					FROM marks
					where studentname='{}'""".format(session['username'])
		results = db.engine.execute(text(sql1))
		return results
	return None


#收集所有的feedback
def infofeedback():
		sql1 = """
					SELECT *
					FROM feedback
					where instructor='{}'""".format(session['username'])
		feedbacks = db.engine.execute(text(sql1))
		return feedbacks

#收集所有的remark信息
def inforemark():
		sql1 = """
					SELECT *
					FROM remark """.format(session['username'])
		remarks = db.engine.execute(text(sql1))
		return remarks

#收集所有的学生成绩
def infoallmark():
		sql1 = """
					SELECT *
					FROM marks """
		marks = db.engine.execute(text(sql1))
		return marks

#判断是否instructor登陆，是返回true
def get_user_type():
	if 'username' in session:
		sql2 = """
					SELECT *
					FROM users
					where username=
					?"""
		results = db.engine.execute(sql2, session['username'])
		for i in results:
			if i[2] == "instructor":
				return True
	return False

# def get_account_type(username):
# 	sql = '''SELECT  from users where username=?'''
# 	db.engine.execute(text(sql), username)
# 	#这里用sql把accounttype根据account取出来
# 	#我没写
# 	return accountype
#
# def if_instructor:
# 	acctype = get_account_type(	acctype = get_account_type())
#学生登陆后的主页
@app.route('/')
def index():
	if 'username' in session:
		if not get_user_type():
			sql1 = """
						SELECT *
						FROM marks
						where studentname='{}'""".format(session['username'])
			results = db.engine.execute(text(sql1))
			return render_template('index.html',data=results, instructor=False)
		else:
			return render_template('index.html', instructor=True)
	else:
		return public()

#登陆页
@app.route('/login',methods=['GET','POST'])
def login():
	if request.method=='POST':
		sql = """
			SELECT *
			FROM users
			"""
		results = db.engine.execute(text(sql))
		for result in results:
			if result['username']==request.form['username']:
				if result['password']==request.form['password']:
					session['username']=request.form['username']
					if not get_user_type():
						sql1 = """
							SELECT *
							FROM marks
							where studentname='{}'""".format(request.form['username'])
						results = db.engine.execute(text(sql1))
						return render_template('index.html',data=results, instructor=False)#登陆成功，返回学生主页
					else:
						return render_template('index.html', instructor=True)
		return public()#登陆未成功，返回公众页面
	elif 'username' in session:
			sql1 = """
					SELECT *
					FROM marks
					where studentname='{}'""".format(session['username'])
			results = db.engine.execute(text(sql1))
			return render_template('index.html',data=results, instructor=False)#已登陆，返回学生主页
	else:
		return render_template('loginPage.html')#返回登录界面

#用于编辑成绩，使用于personal-ins.html，调试成功
#因为是instructor端，所以还没连接到其他页面
@app.route('/editmark',methods=['GET', 'POST'])
def editMark():
	if 'username' in session:
		if request.method=='POST':
			quiz1Mark=request.form['quiz1']
			quiz2Mark=request.form['quiz2']
			quiz3Mark=request.form['quiz3']
			midtermExamMark=request.form['me']
			finalExamMark=request.form['fe']
			username=request.form['studentname']
			updateSQL="""UPDATE marks
				   SET quiz1 = '{}', quiz2 = '{}', quiz3 = '{}',midtermexam = '{}', finalexam = '{}'  
				   WHERE studentname = '{}'""".format(quiz1Mark, quiz2Mark, quiz3Mark, midtermExamMark, finalExamMark, username);
			db.engine.execute(text(updateSQL))
			return redirect(url_for('personalInstructor'))

#用于学生提交remark request
@app.route('/remark',methods=['GET', 'POST'])
def remark():
	if 'username' in session:
		if request.method=='POST':
			quiz1Request=request.form['quiz1']
			quiz2Request=request.form['quiz2']
			quiz3Request=request.form['quiz3']
			midtermExamRequest=request.form['me']
			finalExamRequest=request.form['fe']
			username=session['username']
			if quiz1Request:
				insertSQL="""INSERT INTO remark VALUES('{}', '{}', '{}')""".format('quiz1', username, quiz1Request)
			if quiz2Request:
				insertSQL="""INSERT INTO remark VALUES('{}', '{}', '{}')""".format('quiz2', username, quiz2Request)
			if quiz3Request:
				insertSQL="""INSERT INTO remark VALUES('{}', '{}', '{}')""".format('quiz3', username, quiz3Request)
			if midtermExamRequest:
				insertSQL="""INSERT INTO remark VALUES('{}', '{}', '{}')""".format('midtermExam', username, midtermExamRequest)
			if finalExamRequest:
				insertSQL="""INSERT INTO remark VALUES('{}', '{}', '{}')""".format('finalExam', username, finalExamRequest)
			db.engine.execute(text(insertSQL))
			return redirect(url_for('personal'))


#用于学生写feedback
@app.route('/writefeedback',methods=['GET', 'POST'])
def writefeedback():
	if 'username' in session:
		if request.method=='POST':
			fbInstructor=request.form['feedbackInstructor']
			fbContent1=request.form['feedback1']
			fbContent2=request.form['feedback2']
			fbContent3=request.form['feedback3']
			fbContent4=request.form['feedback4']
			fbContent5=request.form['feedback5']

			insertSQL="""INSERT INTO feedback VALUES('{}', '{}', '{}', '{}', '{}', '{}')""".format(fbInstructor, fbContent1, fbContent2, fbContent3, fbContent4, fbContent5);
			db.engine.execute(text(insertSQL)) 
			return redirect(url_for('feedback'))

#新用户注册界面， 现在不知道为什么显示不出来
@app.route('/createNewuser',methods=['GET','POST'])
def createNewuser():
	if request.method=='POST':
		userType=request.form['type']
		userName=request.form['username']
		passwCode=request.form['password']

		insertSQL1="""INSERT INTO users VALUES('{}', '{}', '{}')""".format(userName, passwCode, userType);
		db.engine.execute(text(insertSQL1))

		insertSQL2="""INSERT INTO marks VALUES('{}', '{}', '{}', '{}', '{}', '{}')""".format('','','','','',userName);
		db.engine.execute(text(insertSQL2))

		return public()

#新用户注册看到的界面, 现在不知道为什么显示不出来
@app.route('/newuser',methods=['GET','POST'])
def newuser():
	return render_template('newuser.html')

#退出登录，在personal界面可以找到
@app.route('/logout')
def logout():
	session.pop('username', None)
	return render_template('public.html', )

#公众页面，信息不开放
@app.route('/public')
def public():
	return render_template('public.html')

#学生个人信息页面
@app.route('/personal',methods=['GET','POST'])
def personal():
	return render_template('personal.html',data=info(), instructor=False)

#学生写feedback的页面
@app.route('/feedback',methods=['GET','POST'])
def feedback():
	return render_template('feedback.html',data=info(), instructor=False)

#instructor查看所有remark request的节目
#instructor给学生remark的界面
#因为是instructor端，所以html还没连接到其他页面
@app.route('/personalInstructor',methods=['GET','POST'])
def personalInstructor():
	return render_template('personal-ins.html',data=inforemark(), instructor=True)

#查看所有学生成绩的地方
@app.route('/allMarks',methods=['GET','POST'])
def allMarks():
	return render_template('allmarks.html',data= infoallmark(), instructor=True)

#instructor查看所有feedback的界面
#因为是instructor端，所以html还没连接到其他页面
@app.route('/feedbackInstructor',methods=['GET','POST'])
def feedbackInstructor():
	return render_template('feedback-ins.html',data=infofeedback(), instructor=True)

#学生登陆后的主页
@app.route('/index',methods=['GET','POST'])
def homepage():
	if not get_user_type():
		return render_template('index.html',data=info(), instructor=False)
	else:
		return render_template('index.html', instructor=True)

#学生登陆后的lab界面
@app.route('/labs',methods=['GET','POST'])
def labs():
	if not get_user_type():
		return render_template('labs.html',data=info(), instructor=False)
	else:
		return render_template('labs.html', instructor=True)

#学生登陆后的lecture界面
@app.route('/lectures',methods=['GET','POST'])
def lectures():
	if not get_user_type():
		return render_template('lectures.html',data=info(), instructor=False)
	else:
		return render_template('lectures.html', instructor=True)

#学生登陆后的syllabus界面
@app.route('/syllabus',methods=['GET','POST'])
def syllabus():
	if not get_user_type():
		return render_template('syllabus.html',data=info(), instructor=False)
	else:
		return render_template('syllabus.html', instructor=True)

#学生登陆后的assignment界面
@app.route('/assignment',methods=['GET','POST'])
def assignment():
	if not get_user_type():
		return render_template('assignment.html',data=info(), instructor=False)
	else:
		return render_template('assignment.html', instructor=True)
	
#学生登陆后的course team界面
@app.route('/courseTeam',methods=['GET','POST'])
def courseTeam():
	if not get_user_type():
		return render_template('courseTeam.html',data=info(), instructor=False)
	else:
		return render_template('courseTeam.html', instructor=True)



if __name__=="__main__":
	app.run(debug=True)





