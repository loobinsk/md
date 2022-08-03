from dateutil.relativedelta import relativedelta
from datetime import datetime

def declination(self, value):
    '''получить правильное склонение'''
    if value % 10 == 1 and value % 100 != 11:
        return 0
    elif 2 <= value % 10 <= 4 and (value % 100 < 10 or value % 100 >= 20):
        return 1
    else:
        return 2

def get_duration(date_start, date_end):
    years_declination = ['год', 'года', 'лет']
    months_declination = ['месяц', 'месяца', 'месяцев']
    days_declination = ['день', 'дня', 'дней']
    date_end = datetime.date(date_end)
    date_start = datetime.date(date_start)
    duration = relativedelta(date_end, date_start)
    duration = f'''{duration.years} {years_declination[declination(duration.years)]}
    {duration.months} {months_declination[declination(duration.years)]} 
    {duration.days} {days_declination[declination(duration.days)]}'''
    return duration
    
