import os
import pickle
import unittest
from pprint import pprint

from src.log import init, project_logger
from src.studyroom import StudyRoomCache
from src.studyroom.query import RoomQuery
from src.studyroom.available import process_reservation_data_in_roomInfo, process_reservation_data_in_roomAvailable
from src.uia.login import get_login_cache, LoginError

# 缓存文件路径
LOGIN_CACHE_FILE = "login-cache.pickle"


def load_cache() -> StudyRoomCache:
    """
    加载 StudyRoom 登录缓存。如果缓存文件不存在，则调用 grab_from_driver 获取新的缓存。
    """
    if os.path.exists(LOGIN_CACHE_FILE):
        with open(LOGIN_CACHE_FILE, "rb") as f:
            login_cache = pickle.load(f)
    else:
        # 如果缓存文件不存在，调用 `get_login_cache` 获取并保存
        login_cache = get_login_cache(cache_grabbers=[StudyRoomCache.grab_from_driver])
        with open(LOGIN_CACHE_FILE, "wb") as f:
            pickle.dump(login_cache, f)

    # 如果对应的缓存为空, 重新调用 grab_from_driver.
    if login_cache.get_cache(StudyRoomCache) is None:
        login_cache = get_login_cache(cache_grabbers=[StudyRoomCache.grab_from_driver])
        with open(LOGIN_CACHE_FILE, "wb") as f:
            pickle.dump(login_cache, f)

    return login_cache


class RoomQueryTest(unittest.TestCase):
    """
    测试 RoomQuery 类的功能

    Tips:
        该测试集是 test_roomInfos 的拓展, 在获得响应字段的基础上进行数据处理.
    """

    def setUp(self):
        init()
        self.cache = load_cache()
        self.query = RoomQuery(self.cache.get_cache(StudyRoomCache))

    def test_available_room(self):
        test_data = self.query.query_room_infos()
        processed_data = process_reservation_data_in_roomInfo(test_data)
        pprint(processed_data)

    def test_available_category_rooms_today(self):
        """
        查询当前类别所有研修间的可用时段, 查询内容为今日.

        请进入此 url 肉眼对照可预约时段结果:
            https://studyroom.ecnu.edu.cn/#/ic/researchSpace/3/3675133/2
                -> redirect to https://studyroom.ecnu.edu.cn/#/ic/home
                -> 普陀校区 -> 普陀研究室 (木门)
        """
        test_data = self.query.query_rooms_available("today")
        processed_data = process_reservation_data_in_roomAvailable(test_data)  # query_date = "today" as default
        pprint(processed_data)

    def test_available_category_rooms_tomorrow(self):
        """
        查询当前类别所有研修间的可用时段, 查询内容为明日.

        请进入此 url 肉眼对照可预约时段结果:
            https://studyroom.ecnu.edu.cn/#/ic/researchSpace/3/3675133/2
                -> redirect to https://studyroom.ecnu.edu.cn/#/ic/home
                -> 普陀校区 -> 普陀研究室 (木门)

        """
        test_data = self.query.query_rooms_available("tomorrow")
        processed_data = process_reservation_data_in_roomAvailable(test_data, "tomorrow")
        pprint(processed_data)

    def test_available_category_rooms_day_after_tomorrow(self):
        """
        查询当前类别所有研修间的可用时段, 查询内容为后天.

        Tips:
            本接口可能存在使用时间限制, 或许在每日 22:00 后才能进行查询.

        请进入此 url 肉眼对照可预约时段结果:
            https://studyroom.ecnu.edu.cn/#/ic/researchSpace/3/3675133/2
                -> redirect to https://studyroom.ecnu.edu.cn/#/ic/home
                -> 普陀校区 -> 普陀研究室 (木门)
        """
        test_data = self.query.query_rooms_available("day_after_tomorrow")
        processed_data = process_reservation_data_in_roomAvailable(test_data, "day_after_tomorrow")
        pprint(processed_data)
