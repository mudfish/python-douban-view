import requests
import csv
import os
from pymysql import *
from lxml import etree
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:123456@127.0.0.1:3306/db_douban")


class spider(object):
    def __init__(self):
        # 电影分页URL
        self.movie_page_url = "https://m.douban.com/rexxar/api/v2/movie/recommend?"
        self.movie_detail_url = "https://movie.douban.com/subject/{}/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
            "Referer": "https://movie.douban.com/explore",
        }
        self.page = 0

    def init(self):
        if not os.path.exists("movie_data.csv"):
            with open("movie_data.csv", "w", newline="") as writer_f:
                writer_f = csv.writer(writer_f)
                writer_f.writerow(
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

    def save_to_csv(self, row):
        with open("movie_data.csv", "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(row)

    def spiderMain(self):
        params = {"start": self.page * 20}
        respJson = requests.get(
            self.movie_page_url, headers=self.headers, params=params
        ).json()
        movie_list = respJson["items"]
        # items从1开始循环
        for i, m in enumerate(movie_list):
            # 此处从第2个开始
            if m["type"] == "movie":
                print("=======正在读取第{}条：".format(i))
                # print(m)
                movie_data = []
                movie_data.append(m["id"])
                movie_data.append(m["title"])
                movie_data.append(m["year"])
                # print(movie_data)
                # print("=====================================")
                # 继续请求电影详情
                movie_detail_response = requests.get(
                    self.movie_detail_url.format(m["id"]), headers=self.headers
                )
                # print(movie_detail_response.text)
                # f = open("movie_detail_response.txt", "w", encoding="utf-8")
                # f.write(movie_detail_response.text)
                path = etree.HTML(movie_detail_response.text)
                # 导演
                movie_data.append(
                    (",".join(path.xpath('//a[@rel="v:directedBy"]/text()')))
                )
                # 主演
                movie_data.append(
                    (",".join(path.xpath('//a[@rel="v:starring"]/text()')))
                )
                # 评分
                movie_data.append(
                    path.xpath('//strong[@property="v:average"]/text()')[0]
                )
                # 封面
                movie_data.append(path.xpath('//img[@rel="v:image"]/@src')[0])
                # 国家
                movie_data.append(
                    path.xpath(
                        '//span[contains(text(),"制片国家")]/following-sibling::br[1]/preceding-sibling::text()[1]'
                    )[0]
                )
                # 摘要
                movie_data.append(
                    path.xpath('//span[@property="v:summary"]/text()')[0].strip()
                )
                # 类型
                movie_data.append(
                    (
                        ",".join(
                            path.xpath(
                                '//div[@id="info"]/span[@property="v:genre"]/text()'
                            )
                        )
                    )
                )
                # 语言
                movie_data.append(
                    path.xpath(
                        '//span[contains(text(),"语言")]/following-sibling::br[1]/preceding-sibling::text()[1]'
                    )[0]
                )
                # 上映日期
                movie_data.append(
                    path.xpath('//span[@property="v:initialReleaseDate"]/text()')[0][
                        :10
                    ]
                )
                # 时长
                movie_data.append(path.xpath('//span[@property="v:runtime"]/text()')[0])
                # url
                movie_data.append(self.movie_detail_url.format(m["id"]))
                self.save_to_csv(movie_data)
                # break
        self.clean_csv()

    def clean_csv(self):
        df = pd.read_csv("movie_data.csv")
        df.dropna(inplace=True)
        df.drop_duplicates()
        # 存储到数据库
        self.save_to_db(df)

    def save_to_db(self, df):
        pd.read_csv("movie_data.csv")
        df.to_sql("tb_movie", con=engine, index=False, if_exists="append")


if __name__ == "__main__":
    spiderObj = spider()
    spiderObj.init()
    spiderObj.spiderMain()
