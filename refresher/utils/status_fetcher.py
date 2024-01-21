import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from .util import print_flush


class StatusFetcher:
    def __init__(self, session: requests.session, wait_time=0.7):
        self.wait_time = wait_time
        self.x = session
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.76",
            "Referer": "https://sso.tju.edu.cn/cas/login?service=http%3A%2F%2Fzhjw.tju.edu.cn%2Flogin.jsp",
        }

    def fetch_single_page(self, date: datetime, idx: int, page_idx: int) -> (list, bool):
        """
        :param date: Date
        :param idx: Num of the class, value in [1,12], integer
        :param page_idx: Num of pages, usually in [1,20], integer
        :return raw_data, has_next?
        """
        query_url = "http://classes.tju.edu.cn/eams/classroom/apply/free!search.action"
        data = {
            'seats': 1,
            'classroom.name': None,
            'cycleTime.cycleCount': 1,
            'cycleTime.cycleType': 1,
            'cycleTime.dateBegin': date.strftime("%Y-%m-%d"),
            'cycleTime.dateEnd': date.strftime("%Y-%m-%d"),
            'roomApplyTimeType': 0,
            'timeBegin': idx,
            'timeEnd': idx,
            'pageNo': page_idx,
        }
        result = self.x.post(query_url, headers=self.headers, data=data)
        # print_flush(result.text)
        soup = BeautifulSoup(result.content, 'lxml')
        rows = soup.select("tr")

        if len(rows) == 0:
            print_flush("==> Unexpected Server Response:")
            print_flush(result)
            print_flush(result.text)
            raise Exception(f'Unknown Exception  {idx} {page_idx}')
        rows.__delitem__(0)

        raw_data = []
        for row in rows:
            values = list(map(lambda e: e.text, row.select("td")))
            if len(values) != 6:
                return [], False
            if values[1] == "" or values[2] == "" or values[3] == "":
                continue
            raw_data.append({
                'campus': values[3],
                'building': values[2],
                'room': values[1],
                'type': values[4],
                'capacity': int(values[5].replace(" ", ""))
            })

        return raw_data, True

    def fetch_class_idx(
            self, date: datetime, idx: int,
            pbar=None
    ) -> list:
        page = 1
        raw_data = []
        if pbar is not None:
            pbar.set_description(f"Start Fetching")
        while True:
            raw, more = self.fetch_single_page(date, idx, page)
            if pbar is not None:
                pbar.set_description(f"fetching page {page}")
            raw_data += raw
            if not more:
                break
            time.sleep(self.wait_time)
            page += 1
        return raw_data

    def fetch_date(self, date: datetime) -> list:
        raw_data = []
        with tqdm(total=12, unit="class") as pbar:
            for i in range(1, 13):
                raw = self.fetch_class_idx(date, i, pbar)
                time.sleep(self.wait_time)
                raw_data.append(raw)
                pbar.update(1)
            pbar.set_description("Finished Fetching Date " + date.strftime("%Y-%m-%d"))
        return raw_data
