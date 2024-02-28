import os
from datetime import date, datetime
from calendar import monthcalendar

from .chrome_driver import ChromeDriver
from app import db
from app.models.match import Match
import app.const as const

from bs4 import BeautifulSoup
import requests

chrome_driver = ChromeDriver()


def get_most_recent_match_date():
    most_recent_match_date = db.session.query(db.func.max(Match.date)).scalar()

    if not most_recent_match_date:
        most_recent_match_date = const.CDL_FIRST_MATCH_DATE

    return most_recent_match_date


def get_match_dates_until_present():
    last_match_date = get_most_recent_match_date()
    last_match_date_month = int(last_match_date.split('-')[1])
    current_date = datetime.now().strftime('%Y-%m-%d')
    current_month = int(current_date.split('-')[1])
    year = const.CDL_YEAR

    if last_match_date_month <= current_month:
        year_month_pairs = [(year, month) for month in range(last_match_date_month, current_month + 1)]
    else:
        range1 = [(year, month) for month in range(last_match_date_month, 13)]
        range2 = [(year + 1, month) for month in range(1, current_month + 1)]
        year_month_pairs = [*range1, *range2]

    days_of_week = [3, 4, 5, 6]

    match_dates = [
        date(year, month, day)
        for year, month in year_month_pairs
        for day_of_week in days_of_week
        for week in monthcalendar(year, month)
        for day in [week[day_of_week]]
        if day != 0
    ]

    return match_dates


def get_urls_by_match_dates():
    match_dates_to_fetch = get_match_dates_until_present()
    return [const.BREAKING_POINT_DATE_URL + match_date.strftime('%Y-%m-%d') for match_date in match_dates_to_fetch]


def parse_match_stage(stage_div):
    stage_element = stage_div.find('a').text.split(' ')
    return ' '.join(stage_element[1:3])


def parse_match_overview(match_overview_div):
    match_overview = {}

    team_names = match_overview_div.find_all('div', class_='mantine-14yjo12')
    match_results = match_overview_div.find('div', class_='mantine-1uguyhf').find_all('div')

    match_overview['team_one'] = team_names[0].find('a').text
    match_overview['team_one_maps_won'] = int(match_results[0].text)
    match_overview['team_two'] = team_names[1].find('a').text
    match_overview['team_two_maps_won'] = int(match_results[2].text)

    return match_overview


def parse_player_data(row):
    player_columns = row.find_all('td')
    return {
        'name': row.find('div', class_='mantine-x468zj').text,
        'kills': int(player_columns[1].text),
        'deaths': int(player_columns[2].text),
        'damage': int(player_columns[5].text.replace(',', '')),
        'objectives': int(player_columns[6].text),
    }


def parse_player_data_for_map(player_data_div):
    player_data_for_map = {
        'team_one_player_data': [],
        'team_two_player_data': []
    }

    player_data_table = player_data_div.find('tbody')
    player_rows = player_data_table.find_all('tr')[1:5] + player_data_table.find_all('tr')[6:10]

    for row in player_rows[:4]:  # Assuming the first team has 4 rows
        player_data_for_map['team_one_player_data'].append(parse_player_data(row))

    for row in player_rows[4:]:  # Assuming the second team starts from the 5th row onwards
        player_data_for_map['team_two_player_data'].append(parse_player_data(row))

    return player_data_for_map


def parse_match_maps(match_maps_overview_div, player_data_by_match_map_divs):
    match_maps = []
    match_maps_overview_divs = match_maps_overview_div.find_all('div', class_='mantine-155beqj')

    for overview_div, player_data_div in zip(match_maps_overview_divs, player_data_by_match_map_divs):
        match_map = {}
        map_results = overview_div.find_all('div', class_='mantine-x468zj')
        match_map['map'] = overview_div.find('div', class_='mantine-6cg8ua').text
        match_map['game_mode'] = overview_div.find('div', class_='mantine-1ey6z4x').text
        match_map['team_one_score'] = int(map_results[0].text)
        match_map['team_two_score'] = int(map_results[2].text)
        match_map.update(parse_player_data_for_map(player_data_div))
        match_maps.append(match_map)

    return match_maps


def parse_match_data(match_url):
    match_page_source = chrome_driver.fetch_match_page_source(match_url)
    soup = BeautifulSoup(match_page_source, 'html.parser')

    match_date = soup.find('div', class_='mantine-7c77qh').text
    stage_div = soup.find('div', class_='mantine-l3a1ir')
    match_overview_div = soup.find('div', class_='mantine-1a5yjft')
    match_maps_overview_div = soup.find('div', class_='mantine-g92whd')
    player_data_by_match_map_divs = soup.find_all('div', class_='mantine-v1hkmm')

    match_data = {
        'match_date': match_date,
        'stage': parse_match_stage(stage_div),
        **parse_match_overview(match_overview_div),
        'match_maps': parse_match_maps(match_maps_overview_div, player_data_by_match_map_divs)
    }

    return match_data


def fetch_match_and_player_data():
    match_date_urls = get_urls_by_match_dates()
    match_urls = chrome_driver.fetch_match_urls_from_match_dates(match_date_urls[6:10])
    match_and_player_data = []

    for match_url in match_urls:
        match_and_player_data.append(parse_match_data(match_url))

    chrome_driver.exit_driver()
    return match_and_player_data

