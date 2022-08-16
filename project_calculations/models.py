import datetime
from django.db import models
from django.contrib.auth.models import User
from project_sales.services import get_duration
from projects import choices
from projects.models import Project
from project_economic_indicators.models import Capex
from project_financing_sources.models import OwnFundVariant, CreditVariant
from project_financing_sources.models import LeasingContractVariant, WorkingCapitalParameter
from project_taxes.models import TaxPrm, DiscountRate
from project_sales.models import SalesInit, OpexVariant
from project_taxes import models as tax_models


class Calculation(models.Model):
	project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='calculation')
	variant_sales = models.ForeignKey(SalesInit, on_delete=models.CASCADE,
									verbose_name='Вариант продаж', related_name='variant_sales',
									blank=True, null=True)
	variant_opexs = models.ForeignKey(OpexVariant, on_delete=models.CASCADE,
									verbose_name='Вариант затрат', related_name='variant_costs',
									blank=True, null=True)
	variant_capex = models.ForeignKey(Capex, on_delete=models.CASCADE,
									verbose_name='Вариант кап. расходов', related_name='variant_capex',
									blank=True, null=True)
	variant_taxs = models.ForeignKey(TaxPrm, on_delete=models.CASCADE,
									verbose_name='Вариант налогов', related_name='variant_taxs',
									blank=True, null=True)
	variant_discount_rate = models.ForeignKey(DiscountRate, on_delete=models.CASCADE,
											verbose_name='Вариант ставки дисконтирования', related_name='variant_discount_rates',
											blank=True, null=True)
	variant_own_funds = models.ForeignKey(OwnFundVariant, on_delete=models.CASCADE,
										verbose_name='Вариант собственного капитала', related_name='variant_own_fund',
										blank=True, null=True)
	variant_credits = models.ForeignKey(CreditVariant, on_delete=models.CASCADE,
									verbose_name='Вариант банковского кредита', related_name='variant_credit',
									blank=True, null=True)
	variant_leasing = models.ForeignKey(LeasingContractVariant, on_delete=models.CASCADE,
									verbose_name='Вариант лизинга', related_name='variant_leasing',
									blank=True, null=True)
	variant_wk = models.ForeignKey(WorkingCapitalParameter, on_delete=models.CASCADE,
									verbose_name='Вариант рабочего капитала', related_name='variant_wk',
									blank=True, null=True)

	def __str__(self):
		return f'Расчет по проекту "{self.project.name}"'

class ProfitAndLossPlan(models.Model):
	calculation = models.ForeignKey(Calculation, on_delete=models.CASCADE)
	month = models.DateTimeField('Месяц, к которому относятся значения')

	revenue = models.FloatField('Выручка')
	cost_price = models.FloatField('Себестоимость')
	gross_profit = models.FloatField('Валовая прибыль')
	business_expenses = models.FloatField('Коммерческие расходы')
	management_expenses = models.FloatField('Управленческие расходы')
	operating_income_ebit = models.FloatField('Операционная прибыль EBIT')
	interest_expenses = models.FloatField('Процентные расходы')
	profit_before_tax = models.FloatField('Прибыль до налогообложения')
	income_tax = models.FloatField('Налог на прибыль')
	net_profit = models.FloatField('Чистая прибыль')
	ebitda = models.FloatField('EBITDA')

	def __str__(self):
		return self.calculation.project.name

class CashFlowPlan(models.Model):
	calculation = models.ForeignKey(Calculation, on_delete=models.CASCADE)
	month = models.DateTimeField('Месяц, к которому относятся значения')

	EBITDA = models.FloatField('EBITDA')
	working_weight_change = models.FloatField('Изменение рабочего капитала')
	income_tax = models.FloatField('Налог на прибыль')
	net_cash_flow_from_operations = models.FloatField('Чистый денежный поток по операционной деятельности')
	payment_capital_costs = models.FloatField('Оплата капитальных расходов')
	VAT_refund = models.FloatField('Возмещение НДС')
	payment_liquidation_expenses = models.FloatField('Оплата ликвидационных расходов')
	receipt_liquidation_proceeds = models.FloatField('Поступление ликвидационных доходов')
	net_cash_flow_from_investing_activities = models.FloatField('Чистый денежный поток по инвестиционной деятельности')
	receipt_from_owners = models.FloatField('Поступление от собственников')
	credit_receipt = models.FloatField('Поступление кредита')
	return_credits = models.FloatField('Возврат кредитов')
	loan_repayment = models.FloatField('Погашение кредита')
	interest_payment = models.FloatField('Оплата процентов')
	net_cash_flow_from_financing_activities = models.FloatField('Чистый денежный поток по финансовой деятельности')
	net_cash_flow = models.FloatField('Чистый денежный поток')
	cash_balance_beginning_period = models.FloatField('Остаток денежных средств на начало периода')
	cash_balance_the_end_period = models.FloatField('Остаток денежных средств на конец периода')

	def __str__(self):
		return self.calculation.project.name

class Balance(models.Model):
	calculation = models.ForeignKey(Calculation, on_delete=models.CASCADE)
	month = models.DateTimeField('Месяц, к которому относятся значения')

	fixed_assets = models.FloatField('Основные средства')
	Total_non_current_assets = models.FloatField('Итого внеоборотные активы')
	Stocks = models.FloatField('Запасы')
	accounts_receivable = models.FloatField('Дебиторская задолженность')
	cash = models.FloatField('Денежные средства')
	total_current_assets = models.FloatField('Итого оборотные активы')
	total_balance = models.FloatField('Итого баланс')
	authorized_share_capital = models.FloatField('Уставный (акционерный) капитал')
	undestributed_profits = models.FloatField('Нераспределенная прибыль')
	total_equity = models.FloatField('Итого собственный капитал')
	borrowed_funds = models.FloatField('Заемные средства')
	accounts_payable = models.FloatField('Кредиторская задолженность')
	total_liabilities = models.FloatField('Итого обязательства')
	Total_balance2 = models.FloatField('Итого баланс')

	def __str__(self):
		return self.calculation.project.name

class ResultFinancialAnalys(models.Model):
	calculation = models.ForeignKey(Calculation, on_delete=models.CASCADE)
	month = models.DateTimeField('Месяц, к которому относятся значения')

	return_on_sales_rot = models.FloatField('Рентабельность продаж (ROS)', null=True, blank=True)
	return_on_equity_roe = models.FloatField('Рентабельность собственного капитала (ROE)', null=True, blank=True)
	return_on_assets_roa = models.FloatField('Рентабельность активов (ROA)', null=True, blank=True)
	asset_turnover_ratio = models.FloatField('Коэффициент оборачиваемости активов', null=True, blank=True)
	current_assets_turnover_ratio = models.FloatField('Коэффициент оборачиваемости оборотных активов', null=True, blank=True)
	inventory_turnover_ratio = models.FloatField('Коэффициент оборачиваемости запасов', null=True, blank=True)
	accounts_receivable_turnover_ratio = models.FloatField('Коэффициент оборачиваемости дебиторской задолженности', null=True, blank=True)
	accounts_payable_turnover_ratio = models.FloatField('Коэффициент оборачиваемости кредиторской задолженности', null=True, blank=True)
	autonomy_coefficient = models.FloatField('Коэффициент автономии', null=True, blank=True)
	leverage_ratio_de = models.FloatField('Коэффициент левериджа (D/E)', null=True, blank=True)
	own_working_capital_ratio = models.FloatField('Коэффициент собственных оборотных средств', null=True, blank=True)
	absolute_liquidity_ratio = models.FloatField('Коэффициент абсолютной ликвидности', null=True, blank=True)
	interim_liquidity_ratio = models.FloatField('Коэффициент промежуточной ликвидности', null=True, blank=True)
	current_liquidity_ratio = models.FloatField('Коэффициент текущей ликвидности', null=True, blank=True)

	def __str__(self):
		return self.calculation.project.name

class Rating(models.Model):
	calculation = models.OneToOneField(Calculation, on_delete=models.CASCADE,related_name='rating')
	rating = models.PositiveIntegerField('Рейтинг проекта', null=True, blank=True)
	comment = models.TextField('Комментарий к рейтингу', null=True, blank=True)

	def __str__(self):
		return self.calculation.project.name

class MainParameter(models.Model):
	calculation = models.OneToOneField(Calculation, on_delete=models.CASCADE,related_name='main_parameters')
	start_date = models.DateField('Начало проекта', null=True, blank=True)
	end_date = models.DateField('Окончание проекта', null=True, blank=True)
	
	def duration(self):
		return get_duration(self.start_date, self.end_date)

	def __str__(self):
		return self.calculation.project.name

class FundingAmount(models.Model):
	calculation = models.OneToOneField(Calculation, on_delete=models.CASCADE, related_name='funding_amounts')
	capEx_amount = models.FloatField('Сумма CapEx (с НДС), руб', null=True, blank=True)
	amount_of_own_funds = models.FloatField('Сумма собственных средств, руб', null=True, blank=True)
	amount_of_borrowed_funds = models.FloatField('Сумма заемных средств, руб', null=True, blank=True)
	DE_ratio = models.FloatField('Коэффициент D/E', null=True, blank=True)
	average_Debt_EBITDA_ratio = models.FloatField('Средний коэффициент Debt/EBITDA', null=True, blank=True)

	def total_amount(self):
		return self.amount_of_own_funds+self.amount_of_borrowed_funds

	def __str__(self):
		return self.calculation.project.name

class AnnualAverage(models.Model):
	calculation = models.OneToOneField(Calculation, on_delete=models.CASCADE,
									related_name='annual_average')
	average_annual_revenue = models.FloatField('Среднегодовая выручка (без НДС), Руб', null=True, blank=True)
	average_annual_operating_costs = models.FloatField('Среднегодовые операционные затраты с амортизайцией (без НДС), руб', null=True, blank=True)
	average_annual_net_profit = models.FloatField('Среднегодовая чистая прибыль, руб', null=True, blank=True)
	average_return_on_sales = models.FloatField('Средняя рентабельность продаж, %', null=True, blank=True)
	average_annual_VAT = models.FloatField('Среднегодовой НДС, руб', null=True, blank=True)
	average_annual_income_tax = models.FloatField('Среднегодовой налог на прибыль, руб', null=True, blank=True)

	def __str__(self):
		return self.calculation.project.name

class BasicIndicator(models.Model):
	calculation = models.OneToOneField(Calculation, on_delete=models.CASCADE,
									related_name='basic_indicators')
	discount_rate = models.FloatField('ставка дисконтирования, %', null=True, blank=True)
	refinancing_rate = models.FloatField('ставка рефинансирования, %', null=True, blank=True)
	net_present_value_npv = models.FloatField('чистая приведенная стоимость npv, руб', null=True, blank=True)
	profitability_index_pi = models.FloatField('индекс рентабельности pi', null=True, blank=True)
	internal_rate_return_irr = models.FloatField('внутренняя норма доходности irr, %', null=True, blank=True)
	MIRR_internal_rate_return = models.FloatField('Модифицированная внутренняя норма доходности MIRR, %', null=True, blank=True)

	def __str__(self):
		return self.calculation.project.name

class PaybackProject(models.Model):
	calculation = models.OneToOneField(Calculation, on_delete=models.CASCADE,
									related_name='payback_project')
	nominal_payback_period = models.TextField('Номинальный срок окупаемости', null=True, blank=True)
	discounted_payback_period = models.TextField('Дисконтированный срок окупаемости', null=True, blank=True)

	def __str__(self):
		return self.calculation.project.name
