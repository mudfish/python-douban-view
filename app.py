from flask import Flask, render_template, request, redirect, url_for, session
from utils import db_query


app = Flask(__name__)
app.secret_key = "mysessionkey"


# 保持数据库连接
# def getconnection():
#     connection.ping(reconnect=True)
#     return connection


# 统一请求拦截
@app.before_request
def before_request():
    # 利用正则匹配，如果/static开头和/login, /logout,/register的请求，则不拦截;其他的判断是否已登录
    if (
        request.path.startswith("/static")
        or request.path == "/login"
        or request.path == "/logout"
        or request.path == "/register"
    ):
        return
    # 如果没有登录，则跳转到登录页面
    if not session.get("login_username"):
        return redirect(url_for("login"))


# 首页
@app.route("/")
def index():
    # 获取电影统计数据
    movie_stats = db_query.fetch_movie_statistics()
    # 获取电影分类统计
    movie_type_distribution = db_query.fetch_movie_type_distribution()
    # 获取电影评分统计
    movie_rating_distribution = db_query.fetch_movie_rating_distribution()
    print(movie_rating_distribution)
    return render_template(
        "index.html",
        login_username=session.get("login_username"),
        movie_stats=movie_stats,
        movie_type_distribution=movie_type_distribution,
        movie_rating_distribution=movie_rating_distribution,
    )


# 登录
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        req_params = dict(request.form)
        # 判断用户名密码是否正确
        sql = "SELECT * FROM `tb_user` WHERE `username` = %s AND `password` = %s"
        params = (req_params["username"], req_params["password"])
        if len(db_query.query(sql, params)) > 0:
            # 存储session
            session["login_username"] = req_params["username"]
            return redirect(url_for("index"))
        else:
            return render_template(
                "error.html",
                error="用户名或密码错误",
            )
    elif request.method == "GET":
        return render_template("login.html")


# 退出
@app.route("/logout")
def logout():
    session.pop("login_username", None)
    return redirect(url_for("index"))


# 注册
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        req_params = dict(request.form)
        if req_params["password"] == req_params["password_confirm"]:
            # 判断是否已存在该用户名
            sql = "SELECT * FROM `tb_user` WHERE `username` = %s"
            params = (req_params["username"],)
            result = db_query.query(sql, params)
            if len(result) > 0:
                return render_template(
                    "error.html",
                    error="用户名已存在",
                )
            sql = "INSERT INTO `tb_user` (`username`, `password`) VALUES (%s, %s)"
            params = (
                req_params["username"],
                req_params["password"],
            )
            db_query.query(sql, params, db_query.QueryType.NO_SELECT)
            return redirect(url_for("login"))
        else:
            return render_template(
                "error.html",
                error="两次密码输入不一致",
            )
    elif request.method == "GET":
        return render_template("register.html")


@app.route("/list")
def movie_list():
    # 查询数据库获取电影列表
    movies = db_query.fetch_movie_list()  # 假设此函数返回一个包含电影信息的列表

    # 渲染并返回list.html，同时传递movies数据
    return render_template("list.html", movies=movies)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def system_error(error):
    return render_template("500.html"), 500


if __name__ == "__main__":
    # 静态文件缓存自动刷新
    app.jinja_env.auto_reload = True
    app.run(host="127.0.0.1", port=8002, debug=True)
