import datetime
import time
from scipy import optimize
import pandas as pd
from dateutil.relativedelta import relativedelta
import functools


def min_date(queryset, obj):
	'''Получить минимальную дату из объектов запроса'''
	if obj=='credits':
		date_list = [obj.date for obj in queryset.all()]
	elif obj=='reciepts':
		date_list = [obj.source_date for obj in queryset.all()]

	if len(date_list)==0:
		return None
	else:
		return min(date_list)

def vat_rate(vat):
	if vat == 0:
		return 0
	elif vat == 1:
		return 0
	elif vat == 2:
		return 10
	else:
		return 20

def compare_dates(date1, date2):
	if date1.strftime("%Y-%m")==date2.strftime("%Y-%m"):
		return True
	else:
		return False


def xnpv(rate, values, dates):
	'''Equivalent of Excel's XNPV function.

	>>> dates = [date(2010, 12, 29), date(2012, 1, 25), date(2012, 3, 8)]
	>>> values = [-10000, 20, 10100]
	>>> xnpv(0.1, values, dates)
	-966.4345...
	'''
	if rate <= -1.0:
		return float('inf')
	d0 = dates[0]    # or min(dates)
	return sum([ vi / (1.0+rate)**((di-d0).days/365.0) for vi, di in zip(values, dates)])

def xirr(values, dates):
	'''Эквивалент функции ЧИСТНДОХ в Excel.

    >>> с даты импорта datetime
    >>> dates = [дата (2010, 12, 29), дата (2012, 1, 25), дата (2012, 3, 8)]
    >>> values = [-10000, 20, 10100]
	'''
	try:
		return optimize.newton(lambda r: xnpv(r, values, dates), 0.0)
	except RuntimeError:
		return optimize.brentq(lambda r: xnpv(r, values, dates), -1.0, 1e10)

def daterange(start_date, end_date, datetime=True):
	'''Получить список дат в периоде

	Keyword arguments:
	start_date -- дата начала периода
	end_date -- дата конца периода
	'''
	if datetime:
		start_date = start_date.date()
		end_date = end_date.date()
	daterange = list(pd.date_range(start_date,
								end_date ,
								freq='M',
								normalize=True,)) #создаем daterange с помощью пандаса

	daterange=[start_date+relativedelta(months=+month) for month in range(len(daterange))] #корректируем дни дат
	if not end_date.strftime("%Y-%m") == daterange[-1].strftime("%Y-%m"): #проверяем, имеется ли последний месяц в списке
		daterange.append(end_date)

	return daterange

def indexing_period(period):
	"""получить кол-во месяцев в периоде индексации.

	Keyword arguments:
	period -- период индексации (полугодие-3,месяц-2, квартал-1, год-0)
	"""
	if period == 3:
		return 6
	elif period == 2:
		return 1
	elif period == 1:
		return 3
	elif period == 0:
		return 12

