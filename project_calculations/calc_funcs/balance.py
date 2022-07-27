from calendar import monthrange
from dateutil.relativedelta import relativedelta
from .intermediate_functions import min_date, daterange
from .intermediate_functions import vat_rate, vat_rate
from .profit_and_loss import ProfitAndLossPlan
from .flow_funds import FlowFunds
from ..models import Balance


class BalanceCalc:
	'''план движения денежных средств'''
	def __init__(self, calculation):
		self.calculation = calculation
		self.FL = FlowFunds(calculation)
		self.PL = ProfitAndLossPlan(calculation)
		self.capex = calculation.variant_capex
		self.borrowed_funds_list = self.borrowed_funds()
		self.authorized_capital_list = self.authorized_capital()
		self.undestributed_profits_list = self.undestributed_profits()

	def fixed_assets(self, month):
		'''получить основные средства'''
		start_value = 0
		values_list = []
		for month, date in enumerate(self.FL.daterange):
			value = start_value+self.FL.receipt_owners(month)
			start_value = value
			if month != self.FL.daterange[0]:
				values_list.append(value)
			else:
				values_list.append(0)

		return values_list[month]

	def total_non_current_assets(self,month):
		'''получить итого внеоборотные активы'''
		return self.fixed_assets(month)

	def stocks(self,month):
		'''получить Запасы'''
		return self.FL.inventory_end(month)

	def liquidation_profit(self, month):
		if month == self.FL.daterange[-1]:
			capex = self.capex
			liquidation_profit = capex.liquidation_profit*choices_vat_rate(capex.liquidation_profit_VAT_rate)/100
			return liquidation_profit
		return 0

	def vat_purchased_assets(self,month):
		'''получить НДС по приобретенным ценностям'''
		vat_balance_end = self.FL.vat_balance_end(month)
		vat_refund = self.FL.VAT_refund(month)
		liq_costs = self.FL.payment_liquidation_expenses(month, vat=True)
		payment_capital_expenses = self.FL.payment_capital_expenses(month,vat=True)
		liquidation_profit = self.liquidation_profit(month)
		total_value = vat_balance_end-vat_refund-liq_costs+payment_capital_expenses+liquidation_profit
		return total_value

	def accounts_receivable(self,month):
		'''получить дебиторскую задолженность'''
		return self.FL.accounting_receivable_end(month)+self.FL.advance_purchase_end(month)

	def cash(self,month):
		'''получить денежные средства'''
		return self.FL.сash_balance_beginning_period(month)

	def total_current_assets(self,month):
		'''получить Итого оборотные активы'''
		return self.stocks(month)+self.vat_purchased_assets(month)+self.accounts_receivable(month)+self.cash(month)

	def total_balance1(self,month):
		'''получить итого баланс'''
		return self.total_non_current_assets(month)+self.total_current_assets(month)

	def authorized_capital(self):
		'''получить уставный (акционерный) капитал'''
		start_value = 0
		values_list = []
		for month, date in enumerate(self.FL.daterange):
			value = start_value+self.FL.receipt_owners(month)
			start_value = value
			if month != self.FL.daterange[0]:
				values_list.append(value)
			else:
				values_list.append(0)

		return values_list

	def undestributed_profits(self):
		'''получить нераспределенную прибыль'''
		start_value = 0
		values_list = []
		for month, date in enumerate(self.FL.daterange):
			value = start_value+self.PL.net_profit(month)
			start_value = value
			if month != self.FL.daterange[0]:
				values_list.append(value)
			else:
				values_list.append(0)

		return values_list

	def total_equity(self,month):
		'''получить итого собственный капитал'''
		return self.authorized_capital_list[month]+self.undestributed_profits_list[month]

	def borrowed_funds(self):
		'''получить заемные средства'''
		start_value = 0
		values_list = []
		for month, date in enumerate(self.FL.daterange):
			value = start_value+self.FL.credit_receipt(month)-self.FL.return_loans(month)
			start_value = value
			if month != self.FL.daterange[0]:
				values_list.append(value)
			else:
				values_list.append(0)

		return values_list

	def accounts_payable(self,month):
		'''получить кредиторскую задолженность'''
		return self.FL.sales_advance_end(month)+self.FL.accounting_payble_end(month)

	def total_liabilities(self,month):
		'''получить итого обязательства'''
		return self.borrowed_funds_list[month]+self.accounts_payable(month)

	def total_balance2(self,month):
		'''получить итого баланс'''
		return self.total_equity(month)+self.total_liabilities(month)

	def add_data_in_db(self):
		'''Добавить все данные в базу данных'''
		for month, date in enumerate(self.FL.daterange):
			model = Balance(month=date,
							fixed_assets = round(self.fixed_assets(month), 2),
							Total_non_current_assets = round(self.total_non_current_assets(month), 2),
							Stocks = round(self.stocks(month), 2),
							accounts_receivable = round(self.accounts_receivable(month), 2),
							cash = round(self.cash(month), 2),
							total_current_assets = round(self.total_current_assets(month), 2),
							total_balance = round(self.total_balance1(month), 2),
							authorized_share_capital = round(self.authorized_capital_list[month], 2),
							undestributed_profits = round(self.undestributed_profits_list[month], 2),
							total_equity = round(self.total_equity(month), 2),
							borrowed_funds = round(self.borrowed_funds_list[month], 2),
							accounts_payable = round(self.accounts_payable(month), 2),
							total_liabilities = round(self.total_liabilities(month), 2),
							Total_balance2=round(self.total_balance2(month),2),
							calculation=self.calculation)
			model.save()
		return f'model'


