from asyncio import subprocess
from datetime import date, datetime, timedelta
from subprocess import call, check_output
from tabnanny import check

from constants import NUM_EMOJIS

PATH_TO_RESERVE = "python3 /Users/tahpramen/Developer/Personal\ Projects/LRT_V2/main.py"
NOW = datetime.now()
END_TIME = datetime(NOW.year, NOW.month, NOW.day, hour=17, minute=0, second=0)

def ceil_dt(dt, delta) -> datetime:
    return dt + (datetime.min - dt) % delta

# call(f"{PATH_TO_RESERVE} {START_TIME} {END_TIME} {DISCORD_USERID}" , shell=True)
# call(f"{PATH_TO_RESERVE} 12:00:00 14:00:00 TahpRamen" , shell=True)
# output = check_output(f"{PATH_TO_RESERVE} 12:00:00 14:00:00 TahpRamen" , shell=True)

def check_output_from_reserve(output):
    if "User not in database" in str(output):
        return False # if false, send dm to user asking for info
    return True # reservation made 

def times_between_xy(start_time:datetime) -> list[datetime]:
    # input format: hh:mm:ss in 24-hour format
    time_delta = 1
    times_between = [start_time]

    if start_time.minute == 30:
        start_time += timedelta(minutes=30)
        times_between.append(start_time)

    while True:
        start_time += timedelta(hours=time_delta)
        times_between.append(start_time)
        if start_time.hour == END_TIME.hour and start_time.minute == END_TIME.minute:
            break 
    times_between.append(datetime(NOW.year, NOW.month, NOW.day, hour=17, minute=30, second=0))
    return times_between
