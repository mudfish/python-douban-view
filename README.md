## 部署说明
0. 导入必要的工具包
1. 创建mysql数据库 `db_douban`，执行doc/`db_douban.sql`
2. 请分别修改db_query.py和main_async.py中的数据库连接信息
3. 首次运行请删除`movie_data.csv`和`page_progress.json`两个文件
4. 运行`main.py`或者异步的`main_async.py`,异步运行会更快，要获取的电影分类和页码请在程序中自行调整：
![alt text](doc/image.png)
5. 爬取完成后，运行`app.py`，然后浏览器访问`http://127.0.0.1:8002/`，用户名密码：admin/123
![alt text](doc/image-1.png)
![alt text](doc/image-2.png)

## 捐赠说明
- 觉得本项目对你有帮助的话，可请作者喝杯茶，谢谢！
  
![alt text](doc/donate.png)

## 更多精彩资源
- 这是一个资源站，后续会不断更新一些好用的东西或书籍教程，值得持续关注：
[https://www.codegen.top/](https://www.codegen.top/)
