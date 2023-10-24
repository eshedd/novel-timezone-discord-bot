import numpy as np
from datetime import datetime, timedelta
import pytz


DAYS = ['First Monday', 'Tuesday', 'Sunday One', 'Second Monday', 'Thursday', 'Saturday', 'Sunday Two']
MONTHS = ['January', 'February', 'March', 'April', 'Quintember', 'June', 'September', 'October', 'November', 'December', 'Amaterasu', 'Apollyon']
year_calendar = [np.arange(10)+1 for _ in range(10)]
year_calendar[1] = np.arange(11)+1
leap_year_calendar = [np.arange(8)+1 for _ in range(12)]
leap_year_calendar[1] = np.arange(14)+1

# ORIGIN = datetime(2023,8,23)
ORIGIN = datetime(2023,8,13)


def get_pure_date(time):
    date = datetime.strptime(time, "%Y/%m/%d")
    direction = np.sign((date - ORIGIN).days)
    year = -1 + (direction < 0)
    numDays = np.abs((date - ORIGIN).days)
    while numDays >= 0+(direction < 0):
        year += 1 
        numDays -= (101 + (year) % 2)

    year, day = direction * year, (direction * numDays) % (101 + (year%2)) + 1

    year_cal = np.arange(1, 111, 10)
    year_cal[:2] -= 1
    leap_year_cal = np.arange(6, 110, 8)
    leap_year_cal[:2] -= 6

    cal = leap_year_cal if year % 2 else year_cal
    month = MONTHS[np.where(cal >= day)[0][0]-1]
    day -= cal[np.where(cal >= day)[0][0]-1]
    return f'{month} {day}, {year} AJ'

def get_pure_now():
    # hawaii = pytz.timezone('US/Hawaii')
    # now = datetime.now().astimezone(hawaii)
    # s = get_pure_date(now.strftime("%Y/%m/%d"))
    # time_since_sunrise = now - timedelta(hours=6, minutes=20)
    taiwan = pytz.timezone('Asia/Taipei')
    now = datetime.now().astimezone(taiwan)
    s = get_pure_date(now.strftime("%Y/%m/%d"))
    time_since_sunrise = now - timedelta(minutes=20)
    total_seconds = (time_since_sunrise.hour*60*60+time_since_sunrise.minute*60+time_since_sunrise.second)
    hour = total_seconds//(100*72)
    minute = total_seconds%(72*100)//72
    second = total_seconds%72
    s = s + f'\n{(len(str(hour))%2*"0")+str(hour)}:{(len(str(minute))%2*"0")+str(minute)}:{(len(str(second))%2*"0")+str(second)} AM\nHappy Sunrise!'
    return s