import json
import math
import datetime
import time
from calendar import monthrange
from scipy import optimize
from dateutil.relativedelta import relativedelta
from project_calculations.models import ProfitAndLossPlan as model
from .intermediate_functions import xirr, vat_rate, compare_dates
from .intermediate_functions import daterange, indexing_period



class ProfitAndLossPlan:
	'''План прибылей и убытков'''

	def __init__(self, calculation):
		'''init calcualtion'''
		self.calculation = calculation
		self.project = calculation.project
		self.sales = calculation.variant_sales
		self.opexs = calculation.variant_opexs.opexs
		self.capex = calculation.variant_capex
		self.taxs = calculation.variant_taxs
		self.discount_rate = calculation.variant_discount_rate
		self.own_funds = calculation.variant_own_funds.own_funds
		self.credits = calculation.variant_credits.credits
		self.leasings = calculation.variant_leasing.leasings
		self.wk = calculation.variant_wk

		self.daterange = daterange(self.sales.start_date, self.sales.end_date)
		self.value_indexation = self.indexation(indexing_period(self.sales.value_indexation_period),
													self.sales.value_indexation)
		self.inflation_indexation = self.indexation(indexing_period(self.sales.inflation_indexation_period),
														self.sales.inflation_indexation)
		self.leasings_costs_list = self.leasings_costs()
		self.leasings_costs_list_minus = self.leasings_costs(minus=True)
		self.income_tax_list = self.income_tax()
		
	def indexation(self, period, indexation_value):
		"""получить список с значениями индексации на каждый месяц в периоде продаж проекта.

		Keyword arguments:
		period -- период индексации (месяц, квартал, год)
		indexation_value -- значение индексации из таблицы sales_init
		"""
		indexation_list = []

		indexation = 1
		for date_index in range(len(self.daterange)):
			if date_index%period==0 and date_index!=0:
				if not date_index in range(period):
					indexation*=indexation_value
			indexation_list.append(indexation)
		return indexation_list

	def depreciation(self, month:int)-> float:
		'''получить аммортизацию проекта'''
		capex = self.capex
		deprication_period = capex.deprication_period #период аммортизации
		if deprication_period != 0 and month <=deprication_period: #Если период амортизации не равен нулю и месяц меньше периода
			if self.daterange[month] >= capex.end_date.date(): #если итерируемая дата меньше даты окончания стройки
				amount_capital_expenditure = capex.amount_capital_expenditure/(1+vat_rate(capex.VAT_rate)/100) #сумма кап. расходов деленная на ндс

				if capex.liquidation_cost_switch: # Если ликвидационная стоимость подлежит амортизации
					amount_capital_expenditure+=capex.liquidation_cost/(1+vat_rate(capex.liquidation_cost_VAT_rate)/100)

				if capex.liquidation_profit_switch:
					amount_capital_expenditure-=capex.liquidation_profit

				credits = self.credits.filter(capitalization=True) #получаем кредиты с капитализацией процентов
				for date in daterange(capex.start_date, capex.end_date):
					amount_capital_expenditure+=self.project_interest_expenses(capex_date=date,queryset=credits) #прибавляем процентные расходы

				return amount_capital_expenditure/deprication_period
		return 0

	def indexed_price(self, month:int)-> float:
		'''Получить иднексируемую стоимость'''
		sales_init = self.sales
		inflation_indexations = self.inflation_indexation[month] #индекс инфляции 
		price = inflation_indexations*sales_init.price
		return price

	def indexed_value(self, month:int)-> float:
		'''Получить иднексируемый объем'''
		sales_init = self.sales
		value_indexations = self.value_indexation[month] # индекс объема
		volume = value_indexations*sales_init.sales_volume
		return volume

	def sales_revenue(self, month:int)-> float:
		'''выручка по продажам'''
		sales_init_vat = 1+vat_rate(self.sales.VAT)/100
		price = self.indexed_price(month) # итого стоимость
		volume = self.indexed_value(month) #итого объема
		revenue = price*volume/sales_init_vat
		return revenue

	def object_revenue(self, month:int)->float:
		'''выручка по объектам'''
		capex_vat = 1+vat_rate(self.capex.liquidation_profit_VAT_rate)/100
		if self.daterange[month] == self.daterange[-1] and not self.capex.liquidation_profit_switch:
			return self.capex.liquidation_profit/capex_vat
		return 0

	#является полем
	def revenue(self, month:int)-> float:
		'''Получить итоговую выручку'''
		sales_revenue = self.sales_revenue(month)
		object_revenue = self.object_revenue(month)
		return sales_revenue+object_revenue

	#является полем для всех расходов
	def amount_expenses(self, queryset, month, add_vat=False):
		'''получить сумму расходов
		Keyword arguments:
		queryset -- qs с опексами
		'''
		opex_price = 0
		for opex in queryset:
			price = opex.price
			if opex.price_indexation:
				price = price*self.inflation_indexation[month]

			if opex.types_business_activity_costs == 1:
				price = price*self.value_indexation[month]

			price = price/(1+vat_rate(opex.VAT_rate)/100)
			if add_vat:
				price*vat_rate(opex.VAT_rate)/100
			opex_price+=price

		return opex_price

	def ndpi(self, month:int)-> float:
		'''Получить ндпи'''
		tax = self.taxs
		if tax.tax_simulation == 1:
			if self.sales.NDPI:
				value = self.indexed_value(month)
				ndpi = value*tax.summ_ndpi*tax.multiplier_ndpi+tax.allowance_ndpi
				return ndpi
		return 0

	def excise(self, month:int)-> float:
		'''Получить акциз'''
		tax = self.taxs
		if tax.tax_simulation == 1:
			if self.sales.excise_duty:
				value = self.indexed_value(month)
				excise = value*tax.summ_excise*tax.multiplier_excise+tax.allowance_excise
				return excise
		return 0

	def liquidation_costs(self, month:int)->float:
		'''получить ликвидационные расходы'''
		costs = 0
		capex = self.capex
		if self.daterange[month] == self.daterange[-1]:#если считаем последний месяц
			costs += capex.liquidation_cost/(1+vat_rate(capex.liquidation_cost_VAT_rate)/100)

		return costs

	def leasing_initial_payment(self, leasing):
		'''получить первоначальный лизинговый платеж'''
		payment = self.capex.amount_capital_expenditure
		if leasing.initial_payment > 0:
			payment = payment*leasing.initial_payment/100

		return payment


	def leasings_costs_for_leasing(self, leasing, minus=False)->list:
		'''получить лизинговые расходы
		считает за весь период и возвращает список'''
		leasing_costs_list = [] #список лизинговых расходов за весь период продаж
		leasing_remainder = self.capex.amount_capital_expenditure
		leasing_index = 0 #индекс для работы с списками платежей и дат лизинга
		for index, month in enumerate(self.daterange): #перебираем все месяца продаж
			leasing_interests = 0 #формируем первоначальный лизинговый расход
			if self.capex.leasing_switch and self.project.fin_source_leasing: #если объект будет в лизинге
				start_date=leasing.contract_start_date.date() #дата контракта
				end_date = leasing.contract_start_date.date()+relativedelta(months=+leasing.term_leasing_contract) #дата конца контракта
				if month >= start_date and month <= end_date: #если дата больше даты начала контракта лизинга и меньше даты окончания контракта
					leasing_month_list = daterange(start_date, end_date, datetime=False) #список дат периода контракт
					if leasing.redemption_sum_general > 0:
						leasing_month_list.append(end_date)
					leasing_month_list.insert(0, start_date)
					leasing_pay_list = [leasing.monthly_lease_payment for month in range(1, leasing.term_leasing_contract)]
					leasing_pay_list.insert(0,-self.capex.amount_capital_expenditure) #добавляем в начало лизинговый платеж
					leasing_pay_list.insert(1,self.leasing_initial_payment(leasing))
					if leasing.redemption_sum_general > 0:
						leasing_pay_list.append(leasing.redemption_sum_general) #добавляем в конец выкупной платеж

					rate = 1+xirr(leasing_pay_list, leasing_month_list) #эффективная ставка
					days=monthrange(month.year, month.month)[1]/365 #количество дней в текущем месяце
					if leasing_index==0:
						days=0

					leasing_cost = (leasing_remainder*rate**days-leasing_remainder)/(1+vat_rate(leasing.VAT_rate)/100) #лизинговый расход
					leasing_interests += leasing_cost #добавляем его в общее значение для всех лизингов
					leasing_index+=1
					leasing_remainder = (leasing_remainder
										+leasing_cost
										*(1+vat_rate(leasing.VAT_rate)/100)
										-leasing_pay_list[leasing_index]) #меняем лизинговый остаток
					if minus:
						leasing_interests-leasing.monthly_lease_payment/(1+vat_rate(leasing.VAT_rate)/100)
			leasing_costs_list.append(leasing_interests) #добавляем итоговые лизинговые расходы 

		return leasing_costs_list

	def leasings_costs(self, minus=False):
		list_=None
		for index, leasing in enumerate(self.leasings.all()):
			costs=self.leasings_costs_for_leasing(leasing)
			print(len(costs))
			if index==0:
				list_ = costs
			else:
				list_ = list(map(sum, zip(list_,costs)))
		return list_




	#является полем
	def cost_price(self, month:int)-> float:
		'''Получить себестоимость
		Keyword arguments:
		month -- итерируемый месяц
		'''
		opexs = self.opexs.all()
		qs = opexs.exclude(cost_types_by_economic_grouping__in=[8, 9]) #исключаем комм. и упр. расходы
		costs = self.amount_expenses(qs, month)
		costs += self.ndpi(month) #добавляем ndpi
		costs += self.excise(month) #добавляем акциз
		costs += self.depreciation(month) #добавляем амортизацию
		costs += self.liquidation_costs(month) #лик. расходы
		costs += self.leasings_costs_list[month] #лизинговые расходы

		return costs

	#является полем
	def gross_profit(self, month:int)-> float:
		'''Получить валовую прибыль'''
		revenue = self.revenue(month) #выручка
		cost = self.cost_price(month) #себестоимость
		return revenue-cost

	#является полем
	def ebit(self, month:int)-> float:
		'''получить EBIT'''
		gross_profit = self.gross_profit(month) #валовая прибыль
		opexs = self.opexs
		commercial_costs = opexs.filter(cost_types_by_economic_grouping=8)
		commercial_costs = self.amount_expenses(commercial_costs,month) #коммерческие расходы
		managerial_costs = opexs.filter(cost_types_by_economic_grouping=9)
		managerial_costs = self.amount_expenses(managerial_costs,month) #управленческие расходы
		ebit = gross_profit-commercial_costs-managerial_costs
		return ebit

	def credit_interest_expenses(self, credit):
		'''получить словарь с процентными расходами по кредиту
		Keyword arguments:
		credit -- объект кредита'''
		interest_expenses_list = {}
		date_in = credit.date_in.date()
		for month in range(credit.grace_period_interest,credit.tenor+1):
			date = date_in+relativedelta(months=+month)
			interest_expense=None
			if credit.calculation_type==0:
				interest_expense = ((credit.sum_in_currancy
									-credit.sum_in_currancy
									/credit.tenor*month)
									*credit.interest_rate/100/12)
			else:
				sum_pay = credit.sum_in_currancy*(
											credit.interest_rate/100/12*(
											1+credit.interest_rate/100/12)**credit.tenor/(
											(1+credit.interest_rate/100/12)**credit.tenor-1))
				interest_expense = sum_pay+(
								(1+credit.interest_rate/100/12)**month)*(
								credit.sum_in_currancy*credit.interest_rate/100/12-sum_pay)

			interest_expenses_list[str(date)]=round(interest_expense,2)
		return interest_expenses_list

	#является полем
	def project_interest_expenses(self, queryset, month=None, capex_date=None):
		'''получить процентный расход по кредитам определенного месяца
		Keyword arguments:
		queryset -- qs с кредитами'''
		total_interest_expenses = 0
		if capex_date:
			date = capex_date
		else:
			date = self.daterange[month]

		for credit in queryset:
			credit = self.credit_interest_expenses(credit) #получаем словарь с проц. расходами
			date = str(date.strftime("%Y-%m"))+'-'+list(credit)[0][-2:]
			expense = credit.get(date,0)# получаем проц. расход за определенную дату
			total_interest_expenses += expense

		return total_interest_expenses

	#является полем
	def project_interest_expenses_all(self, month):
		'''получить процентные расходы по проекту'''
		credits = self.credits.all()
		return self.project_interest_expenses(month=month, queryset=credits)

	#является полем
	def profit_before_tax(self, month:int)-> float:
		'''прибыль до налогооблажения'''
		credits = self.credits.filter(capitalization=False)
		profit = self.ebit(month)-self.project_interest_expenses(month=month, queryset=credits)
		return profit

	def tax_depreciation(self, month:int)-> float:
		'''аммортизация для раcчета налога'''
		capex = self.capex
		if capex.taxdeprication_switch and capex.taxdeprication_period > 0:
			if month <= capex.taxdeprication_period:
				months_tax_depreciation = ((capex.amount_capital_expenditure
											*(1+vat_rate(capex.amortization_premium)/100))
											/(1+vat_rate(capex.VAT_rate)/100)
											/capex.taxdeprication_period)
				return months_tax_depreciation
		return 0

	def tax_liquidation_costs(self, month):
		'''ликвидационные расходы для расчета налога на прибыль'''
		capex = self.capex
		if self.daterange[month]==self.daterange[-1]:
			if capex.liquidation_cost_switch and capex.taxdeprication_switch:
				liquidation_costs=capex.liquidation_cost/(1+vat_rate(capex.liquidation_cost_VAT_rate)/100)
				return liquidation_costs
		return 0

	def tax_liquidation_profit(self, month):
		'''ликвидационные доходы для расчета налога на прибыль'''
		capex = self.capex
		if self.daterange[month]==self.daterange[-1]:
			if capex.liquidation_profit_switch and capex.taxdeprication_switch:
				liquidation_profit=capex.liquidation_profit/(1+vat_rate(capex.liquidation_profit_VAT_rate)/100)
				return liquidation_profit
		return 0

	def depreciation_premium(self, month):
		'''амортизационная прибыль'''
		capex = self.capex
		depreciation_premium = 0
		if capex.taxdeprication_switch and capex.amortization_premium>0:
			depreciation_premium=(capex.amount_capital_expenditure/
									(1+vat_rate(capex.VAT_rate)/100)
									*capex.amortization_premium/100)
		if month==0 and capex.end_date.date() <= self.daterange[0]:
			return depreciation_premium
		else:
			if compare_dates(self.daterange[month], capex.end_date.date()):
				return depreciation_premium
		return 0

	def tax_interest_expenses(self, month):
		'''процентные расходы для расчета налога на прибыль'''
		if self.capex.taxdeprication_switch:
			if month == 0:
				credits = self.credits.filter(capitalization=True)
				return self.project_interest_expenses(month=month,queryset=credits)

		return 0

	def tax_leasings_costs(self, month):
		'''Получить лизинговые расходы для расчета налога на прибыль'''
		leasing_costs = self.leasings_costs_list_minus[month]
		return leasing_costs

	def tax_opexs(self, month):
		'''получить расходы для расчета налога на прибыль'''
		opexs_qs = self.opexs.filter(type_tax=False)
		opexs = self.amount_expenses(opexs_qs, month)
		return opexs

	def tax_profit_before_tax(self, month):
		pbt = self.profit_before_tax(month)
		pbt += self.tax_depreciation(month)
		pbt -= self.tax_liquidation_costs(month)
		pbt += self.tax_liquidation_profit(month)
		pbt -= self.depreciation_premium(month)
		pbt -= self.tax_interest_expenses(month)
		pbt += self.tax_leasings_costs(month)
		pbt += self.tax_opexs(month)
		return pbt


	def income_tax_for_month(self, month):
		profit_before_tax = self.tax_profit_before_tax(month)
		income_tax = 0
		if self.taxs.tax_simulation==0: #если моделирования налогов == min
			if self.taxs.tax_min_burden_base==0:# если база для расчета == выручка
				return self.revenue(month)*self.taxs.tax_min_burden/100
			else:
				income_tax = profit_before_tax*self.taxs.tax_min_burden/100
				return income_tax
		else:
			income_tax = profit_before_tax*self.taxs.income_tax/100
		return income_tax

	def income_tax(self)->list:
		'''получить налог на прибыль'''
		income_tax_list = []
		calculation_frequency = indexing_period(self.taxs.calculation_frequency)#частота расчета
		accumulative_number=0
		for index, month in enumerate(self.daterange):
			if self.taxs.tax_simulation==0:
				accumulative_number+=self.income_tax_for_month(index)#накапливаем налог на прибыль 
				if index%calculation_frequency==0 and accumulative_number>0:
					income_tax_list.append(accumulative_number)#добавляем накопленный налог на прибыль и обнуляем счетчик
					accumulative_number = 0
				else:
					income_tax_list.append(0)
			else: #если моделирование налогов "стандартное"
				income_tax_list.append(self.income_tax_for_month(index))

		return income_tax_list

	#является полем
	def net_profit(self, month:int)-> float:
		'''чистая прибыль'''
		income_tax = self.income_tax_list[month]
		profit = self.profit_before_tax(month)-income_tax
		return profit

	#является полем
	def ebitda(self, month:int)-> float:
		'''ебитда'''
		ebitda = self.ebit(month)+self.depreciation(month)
		return round(ebitda,2)

	def add_data_in_db(self):
		'''Добавить все данные в таблицу ProfitAndLossPlan'''
		opexs = self.opexs
		commercial_costs = opexs.filter(cost_types_by_economic_grouping=8)
		managerial_costs = opexs.filter(cost_types_by_economic_grouping=9)
		time_1 = datetime.datetime.now()
		for month, date in enumerate(self.daterange):
			income_tax = self.income_tax_list[month]
			pf_and_loss_plan = model(month=date,
									revenue = round(self.revenue(month), 2),
									сost_price = round(self.cost_price(month), 2),
									gross_profit = round(self.gross_profit(month), 2),
									business_expenses = round(self.amount_expenses(commercial_costs, month), 2),
									management_expenses = round(self.amount_expenses(managerial_costs, month), 2),
									operating_income_ebit = round(self.ebit(month), 2),
									interest_expenses = round(self.project_interest_expenses_all(month), 2),
									profit_before_tax = round(self.profit_before_tax(month), 2),
									income_tax = round(income_tax, 2),
									net_profit = round(self.net_profit(month), 2),
									ebitda = round(self.ebitda(month), 2),
									calculation=self.calculation,)
			pf_and_loss_plan.save()
		time2=datetime.datetime.now()-time_1
		return 'Все данные успешно добавлены за', time2, 'cек'

	def profit_and_loss_plan(self,month):
		'''получить данные за определенный месяц'''
		data = {}
		opexs = self.calculation.variant_sales.sales_init.opexs
		commercial_costs = opexs.filter(cost_types_by_economic_grouping=8)
		managerial_costs = opexs.filter(cost_types_by_economic_grouping=9)
		credits = self.calculation.variant_credit.credits.all()
		income_tax = self.income_tax_frequency()
		date = self.daterange[month]
		data['выручка']=round(self.revenue(month), 2)
		data['себестоимость']=round(self.cost_price(month), 2)
		data['валовая прибыль']=round(self.cost_price(month), 2)
		data['себестоимость']=round(self.gross_profit(month), 2)
		data['комм. расходы']=round(self.amount_expenses(commercial_costs, month), 2)
		data['упр. расходы']=round(self.amount_expenses(managerial_costs, month), 2)
		data['ebit']=round(self.ebit(month), 2)
		data['проц. расходы']=round(self.project_interest_expenses(date=date, queryset=credits), 2)
		data['прибыль до налогооблажения']=round(self.profit_before_tax(month), 2)
		data['налог на прибыль']=round(income_tax[month], 2)
		data['чистая прибыль']=round(self.net_profit(month), 2)
		data['ебитда']=round(self.ebitda(month), 2)

		return data 