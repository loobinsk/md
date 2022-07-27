from calendar import monthrange
from numpy_financial import ppmt
from dateutil.relativedelta import relativedelta
from .intermediate_functions import min_date, daterange
from .intermediate_functions import vat_rate, compare_dates
from .profit_and_loss import ProfitAndLossPlan
from ..models import CashFlowPlan

class FlowFunds:
	'''план движения денежных средств'''
	def __init__(self, calculation):
		self.PLPlan = ProfitAndLossPlan(calculation)

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

		self.daterange = daterange(self.daterange_min_date(), self.sales.end_date)
		self.change_working_capital = self.change_working_capital()

	def init_sales_count(self):
		if self.daterange[0]<self.PLPlan.daterange[0]:
			delta = relativedelta(self.PLPlan.daterange[0], self.daterange[0])
			return delta.years*12+delta.months
		else:
			return 0

	def sales_count(self, count):
		return count-self.init_sales_count()

	def daterange_min_date(self):
		'''возвращает минимальную дату для таблицы движения ден. средств'''
		sales_start_date = self.sales.start_date
		capex_start_date = self.capex.start_date
		reciept_start_date = min_date(self.own_funds.all(), 'reciepts')
		credit_start_date = min_date(self.credits.all(), 'credits')
		date_list=[sales_start_date, capex_start_date]
		if reciept_start_date:
			date_list.append(reciept_start_date)
		if credit_start_date:
			date_list.append(credit_start_date)
		return min(date_list)

	def EBITDA(self, month):
		'''получить EBITDA'''
		month=self.sales_count(month)
		return self.PLPlan.ebitda(month)

	def days_in_month(self, month):
		year = int(self.daterange[month].strftime("%Y"))
		month_i = int(self.daterange[month].strftime('%m'))
		days = monthrange(year, month_i)[1]
		return days

	def accounting_receivable_end(self, month):
		days = self.days_in_month(month)
		revenue = self.PLPlan.revenue(self.sales_count(month))
		wk = self.wk
		return max([0,
			revenue*days*wk.share_deferred_sales_general/100*wk.turnover_deferred_sales_general/365])

	def sales_advance_end(self, month):
		days = self.days_in_month(month)
		opexs = self.PLPlan.amount_expenses(self.opexs.all(), self.sales_count(month))
		wk = self.wk
		return max([0,
			opexs*days*wk.share_advance_sales_general/100*wk.turnover_advance_sales_general/365])

	def accounting_payble_end(self,month):
		days = self.days_in_month(month)
		opexs = self.PLPlan.amount_expenses(self.opexs.all(), self.sales_count(month))
		wk = self.wk
		return max([0,
			opexs*days*wk.share_different_purchase_general/100*wk.turnover_different_purchase_general/365])

	def advance_purchase_end(self,month):
		days = self.days_in_month(month)
		opexs = self.PLPlan.amount_expenses(self.opexs.all(), self.sales_count(month))
		wk = self.wk
		return max([0,
			opexs*days*wk.share_advance_purchase_general/100*wk.turnover_advance_purchase_general/365])

	def inventory_end(self, month):
		days = self.days_in_month(month)
		opexs = self.PLPlan.amount_expenses(self.opexs.all(), self.sales_count(month))
		wk = self.wk
		return max([0,
			opexs*days*wk.turnover_inventory_general/365])

	def vat_balance_end(self, month):
		days = self.days_in_month(month)
		vat = self.VAT_change(self.sales_count(month))
		wk = self.wk
		return max([0,vat*days*wk.turnover_vat_general/365])

	def VAT_change(self, count):
		qs = self.opexs.all()
		sales_vat = self.PLPlan.revenue(count)*self.sales.VAT/100/(1+vat_rate(self.sales.VAT)/100)
		opex_vat = self.PLPlan.amount_expenses(qs, count, True)
		return sales_vat-opex_vat

	def change_working_capital(self):
		'''получить изменение рабочего капитала на месяц'''
		last_month = 0
		changes_list = []
		for month in range(len(self.daterange)):
			if self.daterange[month]>=self.PLPlan.daterange[0]:
				revenue = self.PLPlan.revenue(self.sales_count(month))

				total_value = 0
				wk = self.wk
				if month == 0:
					start = 0
				else:
					start = last_month
					
				accounting_receivable_end = -self.accounting_receivable_end(month)
				sales_advance_end = self.sales_advance_end(month)
				accounting_payble_end = self.accounting_payble_end(month)
				advance_purchase_end = -self.advance_purchase_end(month)
				inventory_end = -self.inventory_end(month)
				VAT_balance = -self.vat_balance_end(month)
				end = (-accounting_receivable_end
					+sales_advance_end
					-accounting_payble_end
					-advance_purchase_end
					-inventory_end
					-VAT_balance)

				change = end-start
				if month == len(self.daterange) and wk.wc_end_switch:
					total_value += start
				else:
					total_value += change
				if self.project.fin_source_leasing:
					total_value += self.PLPlan.leasings_costs_list[self.sales_count(month)]
					for leasing in self.leasings.all():
						if leasing.distribution_redemption_switch:
							if month != 0 or month != len(self.daterange):
								total_value+=leasing.redemption_sum_general/leasing.term_leasing_contract
				last_month = end

				changes_list.append(round(total_value,2))
			else:
				changes_list.append(0)
		return changes_list

	def income_tax(self, month):
		'''получить налог на прибыль'''
		if self.daterange[month]>self.PLPlan.daterange[0]:
			return self.PLPlan.income_tax_list[self.sales_count(month)]
		else: return 0

	def net_cash_flow_operating_activities(self, month):
		'''получить чистый денежный поток по операционной деятельности'''
		return self.EBITDA(month)+self.change_working_capital[month]+self.income_tax(month)

	def payment_capital_expenses(self, month, vat=False):
		'''получить оплату капитальных расходов'''
		if self.project.financing_type != 3:
			start_date = self.capex.start_date.date()
			end_date = self.capex.end_date.date()
			current_date = self.daterange[month]
			if current_date>start_date and current_date<end_date:
				date_change = (end_date-start_date).days/30
				capex = self.capex.amount_capital_expenditure/date_change
				if vat:
					capex = capex*vat_rate(self.capex.VAT_rate)/100
				return capex

		return 0

	def VAT_refund(self, month):
		'''получить возмещение НДС'''
		capex = self.capex
		current_date = self.daterange[month].strftime("%Y-%m")
		if capex.end_date.strftime("%Y-%m")==current_date:
			if self.project.financing_type != 3:
				if capex.VAT_refund and self.taxs.tax_simulation==1:
					capex_vat=capex.amount_capital_expenditure*capex.VAT_rate/100/(1+vat_rate(capex.VAT_rate)/100)
					return capex_vat

		return 0

	def payment_liquidation_expenses(self, month, vat=None):
		'''Получить оплату ликвидационных расходов'''
		if month == len(self.daterange):
			if self.project.financing_type != 3:
				liq_expenses = -self.capex.liquidation_cost
				if vat:
					liq_expenses*vat_rate(VAT_rate)/100
				return -self.capex.liquidation_cost
		return 0

	def receipt_liquidation_proceeds(self, month):
		'''Получить поступление ликвидационных доходов'''
		if month == len(self.daterange):
			if self.project.financing_type != 3:
				return self.capex.liquidation_profit
		return 0

	def net_cash_flow_investing_activities(self, month):
		'''Получить чистый денежный поток по инвестиционной деятельности'''
		return self.payment_capital_expenses(month)+\
				self.VAT_refund(month)+\
				self.payment_liquidation_expenses(month)+\
				self.receipt_liquidation_proceeds(month)

	def receipt_owners(self, month):
		'''Получить поступление от собственников'''
		own_funds = self.own_funds
		source_sum = 0
		if self.project.fin_source_equity:
			for own_fund in own_funds.all():
				if compare_dates(own_fund.source_date.date(), self.daterange[month]):
					source_sum += own_fund.source_sum

		return source_sum


	def credit_receipt(self, month):
		'''Получить поступление кредита'''
		credits_sum = 0
		if self.project.fin_source_credit:
			for credit in self.credits.all():
				if credit.date_in.strftime("%Y-%m") == self.daterange[month].strftime("%Y-%m"):
					credits_sum += credit.sum_in_currancy

		return credits_sum


	def return_loans(self, month):
		'''Получить возврат кредитов'''
		if self.project.fin_source_credit:
			total_value = 0
			current_date = self.daterange[month]
			for credit in self.credits.all():
				date_end = credit.date_in.date()+relativedelta(months=+credit.tenor)+relativedelta(months=+credit.grace_period_principal)
				if current_date > credit.date_in.date() and current_date < date_end:
					if credit.calculation_type==1:
						total_value += -credit.sum_in_currancy/credit.tenor
					elif credit.calculation_type==0:
						month_i = (date_end-self.daterange[month])/30
						# total_value+=ppmt(credit.interest_rate/100/12, 0, credit.tenor, month_i)

			return total_value

		return 0

	def interest_payment(self, month):
		'''Получить оплату процентов'''
		credits = self.credits.all()
		return -self.PLPlan.project_interest_expenses(credits, month=month)


	def leasing_payment(self, month):
		'''Получить оплату лизинга'''
		capex = self.capex
		leasings = self.leasings.all()
		current_date = self.daterange[month].strftime("%Y-%m")
		for leasing in leasings:
			end_date = leasing.contract_start_date.date()+relativedelta(months=+leasing.term_leasing_contract)
			if self.daterange[month] > leasing.contract_start_date.date() and self.daterange[month] < end_date:
				monthly_lease_payment = -leasing.monthly_lease_payment
				if current_date == leasing.contract_start_date.strftime("%Y-%m"):
					monthly_lease_payment+-leasing.initial_payment*capex.amount_capital_expenditure

				if leasing.distribution_redemption_switch:
					monthly_lease_payment+-leasing.redemption_sum_general/(leasing.contract_start_date.date()-end_date).days/30
				else: 
					if current_date == end_date.strftime("%Y-%m"):
						monthly_lease_payment+-leasing.redemption_sum_general

				return monthly_lease_payment

		return 0

	def net_cash_flow_financing_activities(self, month):
		'''Получить чистый денежный поток по финансовой деятельности'''
		return (
			self.receipt_owners(month)
			+self.credit_receipt(month)
			+self.return_loans(month)
			+self.interest_payment(month)
			+self.leasing_payment(month)
			)

	def net_cash_flow(self, month):
		'''Получить чистый денежный поток'''
		return (
			self.net_cash_flow_operating_activities(month)
			+self.net_cash_flow_investing_activities(month)
			+self.net_cash_flow_financing_activities(month)
			)


	def сash_balance_beginning_period(self, month):
		'''Получить остаток денежных средств на начало периода'''
		if month == 0:
			return 0
		else:
			return self.cash_balance_end_period(month-1, False)

	def cash_balance_end_period(self, month, cycle=True):
		'''Получить остаток денежных средств на конец периода'''
		cash_balance = self.net_cash_flow(month)
		if cycle:
			cash_balance+self.сash_balance_beginning_period(month)
		return cash_balance

	def add_data_in_db(self):
		'''Добавить все данные в базу данных'''
		for month, date in enumerate(self.daterange):
			model = CashFlowPlan(month=date,
								EBITDA = round(self.EBITDA(month), 2),
								working_weight_change = round(self.change_working_capital[month], 2),
								income_tax = round(self.income_tax(month), 2),
								net_cash_flow_from_operations = round(self.net_cash_flow_operating_activities(month), 2),
								payment_capital_costs = round(self.payment_capital_expenses(month), 2),
								VAT_refund = round(self.VAT_refund(month), 2),
								payment_liquidation_expenses = round(self.payment_liquidation_expenses(month), 2),
								receipt_liquidation_proceeds = round(self.receipt_liquidation_proceeds(month), 2),
								net_cash_flow_from_investing_activities = round(self.net_cash_flow_investing_activities(month), 2),
								receipt_from_owners = round(self.receipt_owners(month), 2),
								credit_receipt = round(self.credit_receipt(month), 2),
								return_credits = round(self.return_loans(month), 2),
								loan_repayment = round(0, 2),
								interest_payment = round(self.interest_payment(month), 2),
								net_cash_flow_from_financing_activities = round(self.net_cash_flow_financing_activities(month), 2),
								net_cash_flow = round(self.net_cash_flow(month), 2),
								cash_balance_beginning_period = round(self.сash_balance_beginning_period(month), 2),
								cash_balance_the_end_period = round(self.cash_balance_end_period(month), 2),
								calculation=self.calculation)
			model.save()
		return f'model'

CashFlowPlan
























