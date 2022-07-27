import datetime
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from projects.models import Project
from project_economic_indicators.models import Capex
from projects import choices


class OwnFundVariant(models.Model):
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	variant_name = models.CharField(max_length=255, default='Новый вариант')

	def get_total_own_funds(self):
		value=0
		return value

	def get_count_own_funds(self):
		return self.own_funds.all().count()

class OwnFund(models.Model):
	'''данные о собственном капитале инвестиционного проекта'''
	variant = models.ForeignKey(OwnFundVariant, on_delete=models.CASCADE, related_name='own_funds')
	source_sum = models.FloatField('Сумма вложений',
									validators=[MinValueValidator(0), ],
									default=0,)
	name = models.CharField(max_length=255, default='Новый взнос')
	source_date = models.DateTimeField('Дата вложения собственных средств', blank=True, null=True)
	source_investor = models.CharField('Инвестор',
										max_length=255, blank=True, null=True)
	create_date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.variant.variant_name

class CreditVariant(models.Model):
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	variant_name = models.CharField(max_length=255, default='Новый вариант')

	def total_contributions(self):
		value=0
		return value

class Credit(models.Model):
	'''информация о привлекаемом заемном капитале в инвестиционный проект'''
	variant = models.ForeignKey(CreditVariant, on_delete=models.CASCADE,
								related_name='credits')
	name=models.CharField(max_length=255, default='Новый кредит')
	lender = models.TextField('Банк',
							max_length=350, blank=True, null=True)
	date = models.DateTimeField('Дата договора',
							blank=True, null=True)
	sum_in_currancy = models.FloatField('Сумма',
										validators=[MinValueValidator(0), ],
                                        default=0
                                        )
	date_in = models.DateTimeField('Дата получения', blank=True, null=True)
	capitalization = models.BooleanField('Капитализация процентов', 
										default=False,)
	interest_rate = models.FloatField('Процентная ставка, %',
                                    validators=[MinValueValidator(0), MaxValueValidator(100)],
                                    default=0
                                    )
	tenor = models.PositiveIntegerField('Срок займа, мес.',
							validators=[MinValueValidator(0), ],
                            default=0
                            )
	calculation_type = models.PositiveSmallIntegerField('Тип уплаты',
														choices=choices.CALCULATION_TYPE, default=0)
	grace_period_principal = models.PositiveIntegerField('Грейс-период основного платежа, в мес.',
									default=0,
                                    )
	grace_period_interest = models.PositiveIntegerField('Грейс-период процентных платежей, в мес.',
									default=0,
                                    )
	create_date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.variant.variant_name

	def credit_share(self):
		credits = self.variant.credits.all().count()
		return round(100/credits, 2)


class LeasingContractVariant(models.Model):
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	variant_name = models.CharField(max_length=255, default='Новый вариант')

	def total_pays(self):
		value=0
		return value

class LeasingContract(models.Model):
	'''Договоры лизинга'''
	variant = models.ForeignKey(LeasingContractVariant, on_delete=models.CASCADE, related_name='leasings')
	lessor = models.TextField('Лизингодатель',
							max_length=350,
                            blank=True, null=True)
	name=models.CharField(max_length=255, default='Лизинговая операция')
	object_cost = models.FloatField('Стоимость объекта', default=0, validators=[MinValueValidator(0), ],)
	date_planned_accounting_object = models.DateTimeField('Дата планового учета объекта', blank=True, null=True)
	initial_payment = models.FloatField('Доля первоначального взноса',
										validators=[MinValueValidator(0), ],
                                        default=0,
                                        )
	contract_start_date = models.DateTimeField('Дата договора', blank=True, null=True)
	term_leasing_contract = models.PositiveIntegerField('Срок лизингового договора, мес', default=0)
	monthly_lease_payment = models.FloatField('Ежемесячные лизинговые платежи (с НДС), руб',
												validators=[MinValueValidator(0), ],
	                                            default=0,
                                            )
	redemption_sum_general = models.FloatField('Сумма выкупного платежа',
												validators=[MinValueValidator(0), ],
                                                default=0,
                                                )
	VAT_rate = models.PositiveSmallIntegerField('Ставка ндс',
												choices=choices.RATES, default=0)
	distribution_redemption_switch = models.BooleanField('Распределение выкупного платежа по периодам', default=False)
	create_date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.lessor

	def price_object(self):
		value=0.00
		return value

	def accounting_date(self):
		value=datetime.datetime.now()
		return value

	def total_pays(self):
		value=0
		vat=0
		pays= {
			'value': value,
			'vat': vat,
		}
		return pays

class WorkingCapitalParameter(models.Model):
	'''Параметры расчета рабочего капитала'''
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	variant_name = models.CharField(max_length=255, default='Новый вариант')
	share_deferred_sales_general = models.FloatField('Доля продаж с отсрочкой, %',
									default=0,
                                   	validators=[MinValueValidator(0), MaxValueValidator(100)],
                                    )
	percentage_immediate_pay_sales = models.FloatField('Доля продаж с незамедлительной оплатой',
														validators=[MinValueValidator(0), MaxValueValidator(100)],
														default=0,)
	share_purchases_with_immediate_payment = models.FloatField('Доля закупок с незамедлительной оплатой ',
														validators=[MinValueValidator(0), MaxValueValidator(100)],
														default=0,)
	share_advance_sales_general = models.FloatField('Доля продаж с авансами, %',
									default=0,
									validators=[MinValueValidator(0), MaxValueValidator(100)],	
                                    )
	turnover_deferred_sales_general = models.PositiveIntegerField('Средний срок отсрочки по продажам, дней',
                                    default=0,
                                    validators=[MinValueValidator(0),],
                                    )
	turnover_advance_sales_general = models.PositiveIntegerField('Средний срок авансов от продаж, дней',
									validators=[MinValueValidator(0),],	
									default=0,
                                    )
	share_different_purchase_general = models.FloatField('Доля закупок с отсрочкой платежа, %',
									validators=[MinValueValidator(0), MaxValueValidator(100)],	
                                    default=0,
                                    )
	share_advance_purchase_general = models.FloatField('Доля закупок с авансовыми платежами, %',
														validators=[MinValueValidator(0), MaxValueValidator(100)],	
                                                        default=0,
                                                        )
	turnover_different_purchase_general = models.PositiveIntegerField('Средний срок оплаты поставок, дней',
																	validators=[MinValueValidator(0), ],	
																	default=0,
                                                                    )
	turnover_advance_purchase_general = models.PositiveIntegerField('Срок авансов по закупкам, дней',
																	validators=[MinValueValidator(0), ],	
																	default=0,
                                                                    )
	turnover_inventory_general = models.PositiveIntegerField('Срок оборачиваемости запасов, дней',
									validators=[MinValueValidator(0), ],	
                                    default=0,
                                    )
	turnover_vat_general = models.PositiveIntegerField('Средний срок остатков НДС по приобретенным ценностям (отложенного НДС), в днях',
													validators=[MinValueValidator(0), ],	
                                                    default=0,
                                                    )

	share_cash_sales_general = models.FloatField('Доля продаж с немедленной оплатой, %',
									validators=[MinValueValidator(0), MaxValueValidator(100)],	
									default=0,
                                    )
	wc_end_switch = models.BooleanField('Списывать рабочий капитал в конце проекта', 
										default=False)
	create_date = models.DateTimeField('Дата создания записи', auto_now_add=True)

	def share_of_sales(self):
		value = 0
		return round(value, 2)

	def share_of_purchases(self):
		value = 0
		return round(value, 2)
                            
	def __str__(self):
		return self.variant_name 