from calendar import monthrange
from dateutil.relativedelta import relativedelta

from ..models import MainParameter, FundingAmount
from ..models import AnnualAverage, BasicIndicator
from ..models import PaybackProject, Rating
from project_sales.services import get_duration
from .intermediate_functions import min_date, daterange, vat_rate
from .profit_and_loss import ProfitAndLossPlanCalculation
from .flow_funds import FlowFunds
from .balance import BalanceCalc


class InitData:
	def __init__(self, calculation):
		self.calculation = calculation
		self.FL = FlowFunds(calculation)
		self.PL = ProfitAndLossPlanCalculation(calculation)
		self.BL = BalanceCalc(calculation)
		self.project=calculation.project

class MainParameterCalculation(InitData):

	def start_date(self):
		return self.FL.daterange[0]

	def end_date(self):
		return self.FL.daterange[-1]

class FundingAmountCalculation(InitData):

	def capex_amount(self):
		return self.PL.capex.amount_capital_expenditure

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
		except:
			return None

class AnnualAverageCalculation(InitData):

	def average_annual_revenue(self):
		return 0

	def average_annual_operating_costs(self):
		return 0

	def average_annual_net_profit(self):
		return 0

	def average_return_on_sales(self):
		return 0

	def average_annual_VAT(self):
		return 0

	def average_annual_income_tax(self):
		return 0

class BasicIndicatorCalculation(InitData):

	def discount_rate(self):
		return 0

	def refinancing_rate(self):
		return 0

	def net_present_value_npv(self):
		return 0

	def profitability_index_pi(self):
		return 0

	def internal_rate_return_irr(self):
		return 0

	def MIRR_internal_rate_return(self):
		return 0

class PaybackProjectCalculation(InitData):

	def nominal_payback_period(self):
		return '3 года 7 месяцев 24 дня'

	def discounted_payback_period(self):
		return '1 год 6 месяцев 23 дня'

class ProjectRating(InitData):

	def rating(self):
		return 6

	def comment(self):
		return 'Инвестиционный проект характеризуется хорошей эффективностью. Проект имеет допустимые финансовые риски. Рекомендуется к реализации.'

class DBLoadData(ProjectRating, MainParameterCalculation, 
				FundingAmountCalculation, AnnualAverageCalculation,
				PaybackProjectCalculation, BasicIndicatorCalculation):
	def load_data_in_db(self):
		main_parameter = MainParameter.objects.create(
													start_date=self.start_date(),
													end_date=self.end_date(),
													calculation=self.calculation,
												)
		rating = Rating.objects.create(
									calculation=self.calculation,
									rating = self.rating(),
									comment = self.comment(),
									)
		fundin_gamount = FundingAmount.objects.create(
													calculation=self.calculation,
													capEx_amount=self.capex_amount(),
													amount_of_own_funds=self.amount_of_own_funds(),
													amount_of_borrowed_funds=self.amount_of_borrowed_funds(),
													DE_ratio=self.DE_ratio(),
													average_Debt_EBITDA_ratio=self.average_Debt_EBITDA_ratio(),
													)
		annual_average = AnnualAverage.objects.create(
													calculation=self.calculation,
													average_annual_revenue=self.average_annual_revenue(),
													average_annual_operating_costs=self.average_annual_operating_costs(),
													average_annual_net_profit=self.average_annual_net_profit(),
													average_return_on_sales=self.average_return_on_sales(),
													average_annual_VAT=self.average_annual_VAT(),
													average_annual_income_tax=self.average_annual_income_tax(),
													)
		basic_indicator = BasicIndicator.objects.create(
														calculation=self.calculation,
														discount_rate=self.discount_rate(),
														refinancing_rate=self.refinancing_rate(),
														net_present_value_npv=self.net_present_value_npv(),
														profitability_index_pi=self.profitability_index_pi(),
														internal_rate_return_irr=self.internal_rate_return_irr(),
														MIRR_internal_rate_return=self.MIRR_internal_rate_return(),
														)
		payback_project = PaybackProject.objects.create(
														calculation=self.calculation,
														nominal_payback_period=self.nominal_payback_period(),
														discounted_payback_period=self.discounted_payback_period(),
														)
		return 0




