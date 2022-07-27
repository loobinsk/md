def get_true_list_enums(enums):
	list_enums = []
	for enum in enums:
		list_enum = {}
		list_enum['name'] = enum[1]
		list_enum['id'] = enum[0]
		list_enums.append(list_enum)

	return list_enums

null = 0
_0 = 1
_10 = 2
_20 = 3
RATES = (
	(null, 'Не облагается'),
	(_0, '0'),
	(_10, '10'),
	(_20, '20'),
	)

CapEx = 0
IT = 1
RD = 2
OpEx = 3
FINANCING_TYPE = (
	(CapEx, 'проект капитальных расходов'),
	(IT, 'IT-проект'),
	(RD, 'проект НИОКР'),
	(OpEx, 'проект без капитальных расходов'),
	)

y = 0
q = 1
m = 2
pq = 3
TIME_DETALIZATIONS = (
	(y, 'По годам'),
	(q, 'По кварталам'),
	(m, 'По месяцам'),
	(pq, 'По полугодиям'),
	)

none = 0
th = 1
ml = 2
bl = 3
tl = 4
CURRENCY_MULTIPLICATION = (
	(none, 'Не мультиплицирован'),
	(th, 'В тыс'),
	(ml, 'В млн'),
	(bl, 'В млрд'),
	(tl, 'В трлн'),
	)

min_ = 0
simple = 1
table = 2
TAX_MODEL = (
	(min_, 'минимальный'),
	(simple, 'упрощенный'),
	(table, 'полный'),
	)


_min=0
standart=1
TAX_SIMULATION = (
	(_min, 'минимальное'),
	(simple, 'стандартное'),
	)

y = 0
q = 1
m = 2
VALUE_INDEXATION_PERIOD = (
	(y, 'По годам'),
	(q, 'По кварталам'),
	(m, 'По месяцам'),
	)

PCs = 0
Set = 1
Box = 2
Tone = 3
Units = 4
m3 = 5
Barrel =6
MW = 7
GCal = 8
Service = 9
UNITS = (
	(PCs, 'шт.'),
	(Set, 'компл.'),
	(Box, 'ящ.'),
	(Tone, 'тн.'),
	(Units, 'ед.'),
	(m3, 'м3'),
	(Barrel, 'Баррель'),
	(MW, 'МВт'),
	(GCal, 'Гкал'),
	(Service, 'усл.'),
	)


an = 0
tn = 1
TaxPrmProjectStandartTypes = (
	(y, 'адвалорный налог'),
	(q, 'твердый налог '),
	)

main = 0
additional = 1
FILE_TYPES = (
	(main, 'Основной'),
	(additional, 'Дополнительный'),
	)

mz = 0
products = 1
zp = 2
sosn = 3
am = 4
ppr = 5
ar =6
nr = 7
kr=8
ur = 9
pr = 10
TYPES_BUSINESS_ACTIVITY_COSTS = (
	(mz, 'Материальные затраты'),
	(products, 'Товары'),
	(zp, 'Заработная плата'),
	(sosn, 'Социальное обеспечение и социальные налоги'),
	(am, 'Амортизация'),
	(ppr, 'Прочие производственные расходы'),
	(ar, 'Арендные расходы'),
	(nr, 'Налоговые расходы'),
	(kr, 'Коммерческие расходы'),
	(ur, 'Управленческие расходы'),
	(pr, 'Прочие расходы'),
	)

pnz = 0
pmz = 1
FIXED_ASSET_LEASE_PAYMENT = (
	(pnz, 'Постоянные расходы'),
	(pmz, 'Переменные расходы'),
	)

df = 0
an = 1
CALCULATION_TYPE = (
	(df, 'Дифференцируемый'),
	(an, 'Аннуитетный'),
	)


general = 0
from_table = 1
INDEXATION_TYPE = (
	(df, 'общий'),
	(an, 'Из таблицы'),
	)

sales = 0
costs = 1
opex = 2
taxs = 3
discount_rates = 4
equity = 5
credit=6
leasing=7
TABLES = (
	(sales, 'Вариант продаж'),
	(costs, 'Вариант затрат'),
	(opex, 'Вариант кап. расходов'),
	(taxs, 'Вариант налогов'),
	(discount_rates, 'Вариант ставки дисконтирования'),
	(equity, 'Вариант собственного капитала'),
	(credit, 'Вариант банковского кредита'),
	(leasing, 'Вариант лизинга'),
	)

revenue = 0
profit = 1
TAX_MIN_BURDEN_BASE = (
	(revenue, 'Выручка'),
	(profit, 'Прибыль до налогообложения'),
	)

NDPI = 0
excise = 1
HARD_TAXS = (
	(NDPI, 'НДПИ'),
	(excise, 'Акциз'),
	)
