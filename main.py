import requests
import csv
import os
import json
from pymysql import connect
from lxml import etree
import pandas as pd
from sqlalchemy import create_engine

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "123456",
    "database": "db_douban",
    "port": 3306,
    "charset": "utf8mb4",
}

PAGE_PROGRESS_FILE = "page_progress.json"

MOVIE_TYPES = ["剧情", "喜剧", "动作", "爱情"]

engine = create_engine("mysql+pymysql://root:123456@127.0.0.1:3306/db_douban")

class Spider:
    def __init__(self):
        self.movie_page_url = "https://m.douban.com/rexxar/api/v2/movie/recommend?"
        self.movie_detail_url = "https://movie.douban.com/subject/{}/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
            "Referer": "https://movie.douban.com/explore",
        }
        self.movie_types = MOVIE_TYPES
        self.page_progress = {}

    def init(self):
        if not os.path.exists("movie_data.csv"):
            with open("movie_data.csv", "w", newline="", encoding="utf-8") as writer_f:
                writer = csv.writer(writer_f)
                writer.writerow(
                    [
                        "id",
                        "title",
                        "year",
                        "directors",
                        "casts",
                        "rating",
                        "cover",
                        "country",
                        "summary",
                        "types",
                        "lang",
                        "release_date",
                        "time",
                        "url",
                    ]
                )

    def load_page_progress(self):
        if os.path.exists(PAGE_PROGRESS_FILE):
            with open(PAGE_PROGRESS_FILE, "r", encoding="utf-8") as f:
                self.page_progress = json.load(f)

    def save_page_progress(self):
        with open(PAGE_PROGRESS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.page_progress, f, ensure_ascii=False)

    def get_movie_pages(self, type_name, max_pages=1):
        for page in range(self.page_progress.get(type_name, 1), max_pages+1):
            print('第{}页：'.format(page))
            params = {"start": (page - 1) * 20, "tags": type_name}
            try:
                respJson = requests.get(self.movie_page_url, headers=self.headers, params=params).json()
                movie_list = respJson["items"]
                for m in movie_list:
                    if m["type"] == "movie":
                        self.process_movie(m)
                self.page_progress[type_name] = page+1
                # 记录页面进度
                self.save_page_progress()
            except Exception as e:
                print(f"处理:{type_name}第{page}页失败: {e}")
                break
            

    def process_movie(self, movie):
        movie_data = []
        movie_data.append(movie["id"])
        movie_data.append(movie["title"])
        movie_data.append(movie["year"])
        movie_detail_response = requests.get(self.movie_detail_url.format(movie["id"]), headers=self.headers)
        path = etree.HTML(movie_detail_response.text)
        # 导演
        movie_data.append(",".join(path.xpath('//a[@rel="v:directedBy"]/text()')))
        # 主演
        movie_data.append(",".join(path.xpath('//a[@rel="v:starring"]/text()')))
        # 评分
        movie_data.append(path.xpath('//strong[@property="v:average"]/text()')[0])
        # 封面
        movie_data.append(path.xpath('//img[@rel="v:image"]/@src')[0])
        # 国家
        movie_data.append(path.xpath('//span[contains(text(),"制片国家")]/following-sibling::br[1]/preceding-sibling::text()[1]')[0])
        # 摘要
        movie_data.append(path.xpath('//span[@property="v:summary"]/text()')[0].strip())
        # 类型
        movie_data.append(",".join(path.xpath('//div[@id="info"]/span[@property="v:genre"]/text()')))
        # 语言
        movie_data.append(path.xpath('//span[contains(text(),"语言")]/following-sibling::br[1]/preceding-sibling::text()[1]')[0])
        # 上映日期
        movie_data.append(path.xpath('//span[@property="v:initialReleaseDate"]/text()')[0][:10])
        # 时长
        movie_data.append(path.xpath('//span[@property="v:runtime"]/text()')[0])
        # url
        movie_data.append(self.movie_detail_url.format(movie["id"]))
        self.save_to_csv(movie_data)

    def save_to_csv(self, row):
        with open("movie_data.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(row)

    def clean_csv(self):
        print("清理数据......")
        df = pd.read_csv("movie_data.csv", encoding="utf-8")
        df.drop_duplicates(subset=["id"], keep="first", inplace=True)
        print("存储到数据库......")
        df.to_sql("tb_movie", con=engine, index=False, if_exists="append") 

    def run(self):
        self.init()
        self.load_page_progress()
        for type_name in self.movie_types:
            print(f"获取分类: {type_name}")
            self.get_movie_pages(type_name)
        # 请求结束后，清空页面进度
        # self.page_progress = {}
        # self.save_page_progress()
        self.clean_csv()


if __name__ == "__main__":
    spider = Spider()
    spider.run()