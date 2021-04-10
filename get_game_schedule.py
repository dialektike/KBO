""" KBO 경기 일정을 가져오는 모듈

KBO 경기 일정을 수집합니다. 오늘 경기 일정은 네이버에서 가져오고 있습니다.

Example:
    오늘 경기 일정은 `today()`가 담당합니다.

        >>> import get_game_schedule
        >>> temp = get_game_schedule.today()
        200
        >>> temp
        {'year': '2021', 'date': '04.07', 1: {'away': 'SS', 'home': 'OB', 'state': '18:30'}, 2: {'away': 'LT', 'home': 'NC', 'state': '18:30'}, 3: {'away': 'LG', 'home': 'KT', 'state': '18:30'}, 4: {'away': 'HT', 'home': 'WO', 'state': '18:30'}, 5: {'away': 'HH', 'home': 'SK', 'state': '18:30'}}

"""

import json
from datetime import date

import requests
from bs4 import BeautifulSoup

import parsing_game_schedule


def today():

    temp_url = "https://sports.news.naver.com/kbaseball/schedule/index.nhn"
    req = requests.get(temp_url)
    print(req.status_code)
    html = req.text

    exporting_dict = {}

    soup = BeautifulSoup(html, "lxml")

    exporting_dict = {}

    # 현재 연도를 가져온다.
    today = date.today()
    exporting_dict["year"] = str(today.year)

    # 우선 현재 가져온 자료를 날짜를 찾는다.
    temp_date = soup.find("li", role="presentation", class_="on").find("em").text
    exporting_dict["date"] = temp_date

    # 다음으로 게임 상대를 찾는다.
    todaySchedule = soup.find_all("ul", id="todaySchedule")
    temp_todaySchedule = todaySchedule[0]

    i = 0

    for item in temp_todaySchedule.find_all("li"):
        i = i + 1

        if item.find("div", class_="vs_cnt").find("p", class_="suspended") == None :
            suspended = "0"
        else:
            suspended = item.find("div", class_="vs_cnt").find("p", class_="suspended")

        temp_list = {
            "away": parsing_game_schedule.chang_name_into_id(
                item.find("div", class_="vs_lft").find_all("strong")[0].text,
                exporting_dict["year"],
            ),
            "home": parsing_game_schedule.chang_name_into_id(
                item.find("div", class_="vs_rgt").find_all("strong")[0].text,
                exporting_dict["year"],
            ),
            "state": item.find("div", class_="vs_cnt")
            .find_all("em", class_="state")[0].text.strip(),
            "suspended": suspended
        }
        exporting_dict[i] = temp_list

    return exporting_dict
