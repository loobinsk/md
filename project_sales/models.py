from django.utils import timezone as datetime
from dateutil.relativedelta import relativedelta
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from projects import models as project_models
from projects import choices
from .services import get_duration


def next_month(): return datetime.now()+relativedelta(months=+1)
class SalesInit(models.Model):
	'''данные для моделирования продаж'''
	project = models.ForeignKey(project_models.Project, on_delete=models.CASCADE)
	variant_name = models.CharField(max_length=255, default='Новый вариант')
	product_name = models.TextField('Названия продукции, товаров, услуг', default='Новый продукт')
	product_unit = models.PositiveSmallIntegerField('применяемая единица измерения продукта', 
											choices=choices.UNITS,
                                            default=0)
	start_date = models.DateTimeField('Дата начала продаж',default=datetime.now)
	end_date = models.DateTimeField('Дата окончания продаж',default=next_month)
	sales_volume = models.FloatField('объем продаж в единицах продаж до расчета сезонности и индексации',
                                       default=0,
                                       validators=[MinValueValidator(0)],
                                       )
	VAT = models.PositiveSmallIntegerField('Ставка НДС',
										choices=choices.RATES,
										default=0,
			                            )
	NDPI = models.BooleanField('Облагается НДПИ',
								default=False)
	excise_duty = models.BooleanField('Облагается акцизом',
							default=False)
	value_indexation_period = models.PositiveSmallIntegerField('Частота индексации объема', 
															choices=choices.VALUE_INDEXATION_PERIOD,
															default=0)
	value_indexation = models.FloatField('Значение индексации объема',
										default=1,
                                        validators=[MinValueValidator(0), ])
	inflation_indexation_period = models.PositiveSmallIntegerField('Частота индексации цены на инфляцию',
																	choices=choices.VALUE_INDEXATION_PERIOD,
																	default=0)
	inflation_indexation = models.FloatField('Коэффициент индексации на инфляцию',
											default=1,
		                                    validators=[MinValueValidator(0), ])
	price = models.FloatField('Цена продукции',
							default=0,
                            validators=[MinValueValidator(0), ]
                            )
	def duration(self):
		if self.start_date and self.end_date:
			return get_duration(self.start_date, self.end_date)
		else:
			return '0 лет 0 месяцев 0 дней'

	def __str__(self):
		return self.product_name

class OpexVariant(models.Model):
	project = models.ForeignKey(project_models.Project, on_delete=models.CASCADE)
	variant_name = models.CharField(max_length=255, default='Новый вариант')

	def get_total_opexs(self):
		value = 0
		for opex in self.opexs.all():
			value += opex.price
		vat = 0
		data = {'expenses': value,
				'vat': vat}
		return data

	def __str__(self):
		return self.variant_name

class Opex(models.Model):
	'''Расход проекта'''
	variant = models.ForeignKey(OpexVariant, on_delete=models.CASCADE, related_name='opexs')
	name = models.TextField('Пользовательское название расхода',
							max_length=350,
                            default='Новый расход')
	cost_types_by_economic_grouping = models.PositiveSmallIntegerField('Выбор типа затрат по экономической группировке',
														choices=choices.TYPES_BUSINESS_ACTIVITY_COSTS,
														default=0)
	types_business_activity_costs = models.PositiveSmallIntegerField('Выбор типа затрат по деловой активности',
																	choices=choices.FIXED_ASSET_LEASE_PAYMENT,
																	default=0)
	fixed_asset_lease_payment = models.BooleanField('Идентификатор операционной аренды',
													default=False,)
	tax = models.BooleanField('Идентификатор налогового платежа в составе расходов',
							default=False,)
	type_tax = models.BooleanField('Включать расход в расчет налога на прибыль',
									default=True,)
	price = models.FloatField('Сумма с НДС в месяц, рублей',
												validators=[MinValueValidator(0), ],
                                                default=0
                                                )
	VAT_rate = models.PositiveSmallIntegerField('Ставка НДС',
												choices=choices.RATES,
												default=0,
					                            )
	price_indexation = models.BooleanField('Индексация закупочной цены по продажам', default=False,)
	create_date = models.DateTimeField(auto_now_add=True)

	def get_total_pays(self):
		value=0
		vat=0
		data={'value': value,
			'vat': vat}
		return data

	def __str__(self):
		return self.name