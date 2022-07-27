from dateutil.relativedelta import relativedelta
from datetime import datetime

def get_duration(date_start, date_end):
    date_end = datetime.date(date_end)
    date_start = datetime.date(date_start)
    duration = relativedelta(date_end, date_start)
    code = f'{duration.years} лет {duration.months} месяцев {duration.days} дней'
    return code
    
