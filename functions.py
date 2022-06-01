from asyncio import subprocess
from datetime import date, datetime, timedelta
from os import times
from subprocess import call, check_output
import constants
import requests

PATH_TO_RESERVE = "python3 /Users/tahpramen/Developer/Personal\ Projects/LRT_V2/main.py"
NOW = datetime.now()

def ceil_dt(dt, delta) -> datetime:
    return dt + (datetime.min - dt) % delta

def check_output_from_reserve(output):
    if "User not in database" in str(output):
        return False # if false, send dm to user asking for info
    return True # reservation made 

def times_between_xy(start_time:datetime, end_time:datetime) -> list[datetime]:
    # input format: hh:mm:ss in 24-hour format
    time_delta = 1
    times_between = [start_time]

    if start_time.minute == 30:
        start_time += timedelta(minutes=30)
        times_between.append(start_time)

    if start_time.hour == end_time.hour:
        start_time += timedelta(minutes=30)
        times_between.append(start_time)
    else:
        while True:
            start_time += timedelta(hours=time_delta)
            times_between.append(start_time)
            if start_time.hour == end_time.hour:
                break
    
    if start_time.minute != end_time.minute: 
        times_between.append(datetime(NOW.year, NOW.month, NOW.day, hour=end_time.hour, minute=end_time.minute, second=0))
        
    return times_between

def get_time_slots():
    headers = {
        'authority': 'pacific.libcal.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://pacific.libcal.com',
        'referer': 'https://pacific.libcal.com/spaces',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'lid': '15370',
        'gid': '0',
        'eid': '-1',
        'seat': '0',
        'seatId': '0',
        'zone': '0',
        'accessible': '0',
        'powered': '0',
        'start': str(constants.TODAY),
        'end': str(constants.TODAY_PLUS_THREE),
        'pageIndex': '0',
        'pageSize': '18',
    }
    response = requests.post('https://pacific.libcal.com/spaces/availability/grid', headers=headers, data=data)
    json_object = response.json()
    return json_object["slots"]

def find_last_time_of_day(time_slots_json):
    room_data = dict() 
    for i in range(len(time_slots_json)):
        if time_slots_json[i]['itemId'] == constants.ROOMS[107]:
            start_time = time_slots_json[i]['start']
            slot_info = time_slots_json[i]
            room_data[start_time] = slot_info
    
    available_times = []
    for i in room_data.keys():
        if str(constants.TODAY) in i:
            available_times.append(i)
        else:
            break
    # print(f"Last time of day: {available_times[-1]}")
    if len(available_times) != 0:
        date_time_str = available_times[-1]
        date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
        return date_time_obj
    else:
        return None
