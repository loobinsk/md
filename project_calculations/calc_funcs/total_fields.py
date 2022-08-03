from calendar import monthrange
from dateutil.relativedelta import relativedelta

from ..models import MainParameter, FundingAmount
from ..models import AnnualAverage, BasicIndicator
from ..models import PaybackProject
from project_sales.services import get_duration
from .intermediate_functions import min_date, daterange, vat_rate
from .profit_and_loss import ProfitAndLossPlan
from .flow_funds import FlowFunds
from .balance import BalanceCalc


class InitData:
	def __init__(self, calculation):
		self.calculation = calculation
		self.FL = FlowFunds(calculation)
		self.PL = ProfitAndLossPlan(calculation)
		self.BL = BalanceCalc(calculation)
		self.project=calculation.project

class MainParameterCalculation(InitData):

	def duration(self):
		return get_duration(self.FL.daterange[0], self.FL.daterange[-1])

	def start_date(self):
		return self.FL.daterange[0]

	def end_date(self):
		return self.FL.daterange[-1]

class FundingAmountCalculation(InitData):

	def capex_amount(self):
		return self.PL.capexs.amount_capital_expenditure

	def amount_of_own_funds(self):
		total_value = 0
		if self.project.fin_source_equity:
			for own_fund in self.PL.own_funds.all():
				total_value+=own_fund.source_sum

		return total_value

	def amount_of_borrowed_funds(self):
		total_value=0
		if self.project.fin_source_credit:
			for credit in self.PL.credits.all():
				total_value+=credit.sum_in_currancy

		return total_value

	def DE_ratio(self):
		try:
			return self.amount_of_borrowed_funds()/self.amount_of_own_funds()
		except ZeroDivisionError:
			return None

	def average_Debt_EBITDA_ratio(self):
		try:
			amount_of_borrowed_funds = sum(self.BL.borrowed_funds_list)/len(self.FL.daterange)
			total_ebitda = self.PL.total_ebitda_in_all_month()
			return amount_of_borrowed_funds/total_ebitda
		except ZeroDivisionError:
			return None

class AnnualAverageCalculation(InitData):

	def average_annual_revenue(self):
		pass

	def average_annual_operating_costs(self):
		pass

	def average_annual_net_profit(self):
		pass

	def average_return_on_sales(self):
		pass

	def average_annual_VAT(self):
		pass

	def average_annual_income_tax(self):
		pass

class BasicIndicatorCalculation(InitData):

	def discount_rate(self):
		pass

	def refinancing_rate(self):
		pass

	def net_present_value_npv(self):
		pass

	def profitability_index_pi(self):
		pass

	def internal_rate_return_irr(self):
		pass

	def MIRR_internal_rate_return(self):
		pass

class PaybackProjectCalculation(InitData):

	def nominal_payback_period(self):
		pass

	def discounted_payback_period(self):
		pass

class ProjectRating(InitData):

	def rating(self):
		pass

	def comment(self):
		pass

class DBLoadData(ProjectRating, MainParameterCalculation, 
				FundingAmountCalculation, AnnualAverageCalculation,
				PaybackProjectCalculation, BasicIndicatorCalculation):
	def load_data_in_db(self):



