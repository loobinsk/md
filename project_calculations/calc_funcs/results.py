from .intermediate_functions import min_date, daterange, vat_rate
from .profit_and_loss import ProfitAndLossPlanCalculation
from .flow_funds import FlowFunds
from .balance import BalanceCalc
from calendar import monthrange
from dateutil.relativedelta import relativedelta
from ..models import ResultFinancialAnalys

class FinancialAnalysisResult:
	'''план движения денежных средств'''
	def __init__(self, calculation):
		self.calculation = calculation
		self.FL = FlowFunds(calculation)
		self.PL = ProfitAndLossPlanCalculation(calculation)
		self.BL = BalanceCalc(calculation)
		self.project=calculation.project
		self.sales_count = self.FL.sales_count

	def return_on_sales_rot(self, month):
		'''Рентабельность продаж'''
		try:
			return self.PL.net_profit(self.sales_count(month))/self.PL.revenue(self.sales_count(month))*100
		except ZeroDivisionError:
			return 0

	def return_on_equity_roe(self, month):
		'''Рентабельность собственного капитала'''
		net_profit=self.PL.net_profit(self.sales_count(month))
		tq = self.BL.total_equity(month)*100
		try:
			return net_profit/tq
		except ZeroDivisionError:
			return 0

	def return_on_assets_roa(self, month):
		'''Рентабельность активов'''
		try:
			return self.PL.net_profit(self.sales_count(month))/self.BL.total_balance1(month)*100
		except ZeroDivisionError:
			return 0

	def asset_turnover_ratio(self, month):
		'''Коэффициент оборачиваемости активов'''
		try:
			return self.PL.net_profit(self.sales_count(month))/self.BL.total_balance1(month)
		except ZeroDivisionError:
			return 0


	def current_assets_turnover_ratio(self, month):
		'''Коэффициент оборачиваемости оборотных активов'''
		try:
			return self.PL.net_profit(self.sales_count(month))/self.BL.total_current_assets(month)
		except ZeroDivisionError:
			return 0

	def inventory_turnover_ratio(self, month):
		'''Коэффициент оборачиваемости запасов'''
		try:
			return self.PL.cost_price(self.sales_count(month))/self.BL.stocks(month)
		except ZeroDivisionError:
			return 0

	def accounts_receivable_turnover_ratio(self, month):
		'''Коэффициент оборачиваемости дебиторской задолженности'''
		try:
			return self.PL.net_profit(self.sales_count(month))/self.BL.accounts_payable(month)
		except ZeroDivisionError:
			return 0

	def accounts_payable_turnover_ratio(self, month):
		'''Коэффициент оборачиваемости кредиторской задолженности'''
		try:
			return self.PL.cost_price(self.sales_count(month))/self.BL.accounts_payable(month)
		except ZeroDivisionError:
			return 0


	def autonomy_coefficient(self, month):
		'''Коэффициент автономии'''
		try:
			return self.BL.total_equity(month)/self.BL.total_balance2(month)
		except ZeroDivisionError:
			return 0

	def leverage_ratio_de(self, month):
		'''Коэффициент левериджа (D/E)'''
		if not self.project.fin_source_credit:
			return 0
		else:
			try:
				return self.BL.total_equity(month)/self.BL.borrowed_funds_list[month]
			except ZeroDivisionError:
				return 0

	def own_working_capital_ratio(self, month):
		'''Коэффициент собственных оборотных средств'''
		try:
			return (self.BL.total_equity(month)-self.BL.total_non_current_assets(month))/self.BL.total_current_assets(month)
		except ZeroDivisionError:
			return 0

	def absolute_liquidity_ratio(self, month):
		'''Коэффициент абсолютной ликвидности'''
		try:
			return self.BL.cash(month)/self.BL.accounts_payable(month)
		except ZeroDivisionError:
			return 0

	def interim_liquidity_ratio(self, month):
		'''Коэффициент промежуточной ликвидности'''
		try:
			return (self.BL.cash(month)+self.FL.accounting_receivable_end(month))/self.BL.accounts_payable(month)
		except ZeroDivisionError:
			return 0


	def current_liquidity_ratio(self, month):
		'''Коэффициент текущей ликвидности'''
		try:
			return self.BL.total_current_assets(month)/self.BL.accounts_payable(month)
		except ZeroDivisionError:
			return 0


class ResultsDBLoadData(FinancialAnalysisResult):
	def add_data_in_db(self):
		'''Добавить все данные в базу данных'''
		for month, date in enumerate(self.FL.daterange):
			model = ResultFinancialAnalys(month=date,
										return_on_sales_rot = round(self.return_on_sales_rot(month), 2),
										return_on_equity_roe = round(self.return_on_equity_roe(month), 2),
										return_on_assets_roa = round(self.return_on_assets_roa(month), 2),
										asset_turnover_ratio = round(self.asset_turnover_ratio(month), 2),
										current_assets_turnover_ratio = round(self.current_assets_turnover_ratio(month), 2),
										inventory_turnover_ratio = round(self.inventory_turnover_ratio(month), 2),
										accounts_receivable_turnover_ratio = round(self.accounts_payable_turnover_ratio(month), 2),
										accounts_payable_turnover_ratio = round(self.accounts_payable_turnover_ratio(month), 2),
										autonomy_coefficient = round(self.autonomy_coefficient(month), 2),
										leverage_ratio_de = round(self.leverage_ratio_de(month), 2),
										own_working_capital_ratio = round(self.own_working_capital_ratio(month), 2),
										absolute_liquidity_ratio = round(self.absolute_liquidity_ratio(month), 2),
										interim_liquidity_ratio = round(self.interim_liquidity_ratio(month), 2),
										current_liquidity_ratio = round(self.current_liquidity_ratio(month), 2),
										calculation=self.calculation)
			model.save()
		return f'model'
