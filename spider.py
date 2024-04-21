import requests
import csv
import os
from pymysql import *


class spider(object):
    def __init__(self):
        # 电影分页URL
        self.movie_page_url = "https://m.douban.com/rexxar/api/v2/movie/recommend?"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
            "Referer": "https://movie.douban.com/explore",
        }
        self.page = 0

    def init(self):
        if not os.path.exists("./tempData.csv"):
            with open("./tempData.csv", "w", newline="") as writer_f:
                writer_f = csv.writer(writer_f)
                writer_f.writerow(
                    [
                        "id",
                        "title",
                        "year",
                        "directors",
                        "rating",
                        "cover",
                        "country",
                        "summary",
                        "types",
                        "lang",
                        "time",
                        "casts",
                        "url",
                    ]
                )
        # try:
        #     conn = connect(
        #         host="localhost",
        #         user="root",
        #         password="123456",
        #         database="db_douban",
        #         port=3306,
        #         charset="utf8mb4",
        #     )

        # except:
        #     print("An exception occurred")

    def spiderMain(self):
        params = {"start": self.page * 20}
        respJson = requests.get(
            self.movie_page_url, headers=self.headers, params=params
        ).json()
        print(respJson)


if __name__ == "__main__":
    spiderObj = spider()
    spiderObj.init()
    spiderObj.spiderMain()
