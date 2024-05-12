from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql.cursors



# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='123456',
                             db='user_test',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    
app = Flask(__name__)

# 保持数据库连接
def getconnection():
    connection.ping(reconnect=True)
    return connection
    
# 首页
@app.route('/')
def index():
    try:
        with getconnection().cursor() as cursor:
            sql = "SELECT * FROM `tb_user`"
            cols = ['id', 'name', 'age','gender','phone']
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()
            return render_template("index.html", items=result, cols=cols, success='')
    except Exception as e:
        cursor.close()
        return render_template("index.html", items=[], cols=[], success='Can\'t view index: ' + str(e))
    
# 搜索
@app.route('/search')
def search():
    keyword = request.args.get('keyword').strip()
    try:
        with getconnection().cursor() as cursor:
            sql = "SELECT * FROM `tb_user` where name like concat('%%',%s,'%%')"
            cols = ['id', 'name', 'age','gender','phone']
            cursor.execute(sql,(keyword))
            result = cursor.fetchall()
            # print(result)
            cursor.close()
            return render_template("index.html", items=result, keyword=keyword, cols=cols, success='')
    except Exception as e:
        cursor.close()
        return render_template("index.html", items=[], cols=[], success='search error: ' + str(e))


@app.route('/toAddPage')
def toAddPage():
 return render_template('add.html')

@app.route('/toEditPage/<int:id>')
def toEditPage(id):
    # print(id)
    try:
        with getconnection().cursor() as cursor:
            sql = "select * from `tb_user` where id=%s"
            cursor.execute(sql, (id))
            result = cursor.fetchone()
            cursor.close()
            return render_template("edit.html", item=result, success='')
    except Exception as e:
        cursor.close()
        return render_template("edit.html", success='Can\'t edit User: ' + str(e))

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name'].strip()
    age = request.form['age'].strip()
    gender = request.form['gender'].strip()
    phone = request.form['phone'].strip()
    try:
        with getconnection().cursor() as cursor:
            sql = "INSERT INTO `tb_user` (`name`, `age`,`gender`,`phone`) VALUES (%s, %s,%s,%s)"
            cursor.execute(sql, (name, age,gender,phone))
            cursor.close()
            return redirect(url_for("index"))
    except Exception as e:
        cursor.close()
        return render_template("add.html", success='Can\'t add User: ' + str(e))

@app.route('/edit',methods=['POST'])
def edit():
    id = request.form['id'].strip()
    name = request.form['name'].strip()
    age = request.form['age'].strip()
    phone = request.form['phone'].strip()
    gender = request.form['gender'].strip()
    try:
        with getconnection().cursor() as cursor:
            sql = "update `tb_user` set name=%s,age=%s,gender=%s,phone=%s where id=%s"
            cursor.execute(sql, (name, age,gender,phone,id))
            cursor.close()
            return redirect(url_for("index"))
    except Exception as e:
        cursor.close()
        return render_template("edit.html", success='Can\'t edit User: ' + str(e))

@app.route('/remove/<int:id>/')
def remove(id):
    try:
        with getconnection().cursor() as cursor:
            sql = "delete from `tb_user` where id=%s"
            cursor.execute(sql, (id))
            cursor.close()
            return redirect(url_for("index"))
    except Exception as e:
        cursor.close()
        return render_template("index.html", success='Can\'t remove User: ' + str(e))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@app.errorhandler(500)
def system_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # 静态文件缓存自动刷新
    app.jinja_env.auto_reload = True
    app.run(host='127.0.0.1',port=8001, debug=True)