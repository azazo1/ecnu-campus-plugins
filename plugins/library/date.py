"""
图书馆特定区域的可预约时间对象, 见 $projectdir/test/test_library/query_date_example.json 文件.
"""
from typing import Self

from datetime import time, datetime


class Day:
    """
    可选日期, 其下有多个可选时间段.
    """

    def __init__(self, json_data: dict):
        """
        Parameters:
            json_data: 包含 day 和 times 字段的对象.
        """
        self.raw = json_data
        day_ = self.raw["day"]
        self.day = datetime.strptime(day_, "%Y-%m-%d").date()
        self.times = TimePeriod.from_response_part(self.raw["times"], self)

    @classmethod
    def from_response(cls, json_data: list[dict]) -> list[Self]:
        """
        从 date 请求返回的 json 中提取多个 Day.
        """
        rst = []
        for obj in json_data:
            rst.append(Day(obj))
        return rst

    def __repr__(self):
        return repr(self.raw)

    def __getitem__(self, item):
        return self.raw[item]


class TimePeriod:
    """一天中的可选时间段."""

    def __init__(self, json_data: dict, day: Day):
        """
        Parameters:
            json_data: 一个 times 中的对象.
        """
        self.raw = json_data
        self.id = int(self.raw['id'])
        start = self.raw['start']
        end = self.raw['end']
        self.day = day
        self.start = time(*[int(i) for i in start.split(':', maxsplit=2)])
        self.end = time(*[int(i) for i in end.split(':', maxsplit=2)])

    @classmethod
    def from_response_part(cls, part: list, day):
        """从 date 请求返回 json 中的 times 字段提取出多个 Time. """
        return [TimePeriod(p, day) for p in part]

    def __getitem__(self, item):
        return self.raw[item]

    def __repr__(self):
        return repr(self.raw)
