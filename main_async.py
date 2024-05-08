import requests
import csv
import os
import json
from pymysql import connect
from lxml import etree
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
import aiohttp
import asyncio
from aiohttp import ClientSession
from tqdm import tqdm
import time

# 本次运行获取的最大页数
MAX_PAGES = 3
# 进度控制文件
PAGE_PROGRESS_FILE = "page_progress.json"
# 电影类型
MOVIE_TYPES = ["剧情", "喜剧", "动作", "爱情"]
# CSV文件名
CSV_NAME = "movie_data.csv"
# CSV头
CSV_HEADS = ["id","title","year","directors","casts","rating","cover","country","summary","types","lang","release_date","time","url",]

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
        # 需要抓取的页面数
        self.total_pages = 0
        self.completed_pages = 0
        self.global_progress_bar = None

    def init(self):
        # 每次跑之前，先删除之前的csv文件
        if os.path.exists(CSV_NAME):
            os.remove(CSV_NAME)    
        with open(CSV_NAME, "w", newline="", encoding="utf-8") as writer_f:
            writer = csv.writer(writer_f)
            writer.writerow(CSV_HEADS)

    def load_page_progress(self):
        if os.path.exists(PAGE_PROGRESS_FILE):
            with open(PAGE_PROGRESS_FILE, "r", encoding="utf-8") as f:
                self.page_progress = json.load(f)

    def save_page_progress(self):
        with open(PAGE_PROGRESS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.page_progress, f, ensure_ascii=False)

    async def get_movie_pages(self, session, type_name):
        start_page = self.page_progress.get(type_name, 1)
        if(start_page<=MAX_PAGES):
            for page in range(start_page, MAX_PAGES+1):
                # print(f'{type_name}第{page}页：')
                start_time = time.time()
                params = {"start": (page - 1) * 20,"count":10, "tags": type_name}
                try:
                    async with session.get(self.movie_page_url, headers=self.headers, params=params) as resp:
                        resp.raise_for_status()
                        respJson = await resp.json()
                        movie_list = respJson["items"]
                        for i,m in enumerate(movie_list):
                            if m["type"] == "movie":
                                await self.process_movie(session,m)
                                #progress_bar.update(round(1/len(movie_list)))
                        self.page_progress[type_name] = page+1
                        # 记录进度
                        self.save_page_progress()
                        # 刷新全局进度
                        self.update_global_progress()
                except Exception as e:
                    print(f"处理:{type_name}第{page}页失败: {e}")
                    break
 
    async def process_movie(self, session, movie):
        movie_data = []
        movie_data.append(movie["id"])
        movie_data.append(movie["title"])
        movie_data.append(movie["year"])
        async with session.get(self.movie_detail_url.format(movie["id"]), headers=self.headers) as resp:
            resp.raise_for_status()
            html_text =  await resp.text()
        path = etree.HTML(html_text)
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
        with open(CSV_NAME, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(row)

    def clean_csv(self):
        print("===========清理数据============")
        df = pd.read_csv(CSV_NAME, encoding="utf-8")
        df.drop_duplicates(subset=["id"], keep="first", inplace=True)
        print("存储到数据库...")
        df.to_sql("tb_movie", con=engine, index=False, if_exists="append") 
        print('清理重复数据...')
        engine.connect().execute(text("delete from tb_movie where id in (select id from (select id from tb_movie group by id having count(*) > 1) as t)"))

    def update_global_progress(self):
        self.completed_pages += 1
        #print(self.completed_pages)
        self.global_progress_bar.update(self.completed_pages)
        self.global_progress_bar.refresh()
        
    async def run(self):
        self.init()
        self.load_page_progress()
        #self.total_pages = MAX_PAGES*len(MOVIE_TYPES) - sum(self.page_progress.get(type_name, 1) for type_name in MOVIE_TYPES)
        for type_name in MOVIE_TYPES:
            if MAX_PAGES > self.page_progress.get(type_name, 1):
                self.total_pages+=MAX_PAGES+1-self.page_progress.get(type_name, 1)
        # print(self.total_pages)
        if self.total_pages > 0:
            self.global_progress_bar = tqdm(total=self.total_pages, desc="progress", unit="page", colour='GREEN')
            
            async with aiohttp.ClientSession() as session:
                tasks = [self.get_movie_pages(session, type_name) for type_name in self.movie_types]
                await asyncio.gather(*tasks)
            # 请求结束后，清空页面进度
            # self.page_progress = {}
            # self.save_page_progress()
            self.global_progress_bar.close()
            self.clean_csv()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    spider = Spider()
    loop.run_until_complete(spider.run())