from django.utils import timezone as datetime
from dateutil.relativedelta import relativedelta
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from projects.models import Project
from projects import choices

from project_sales.services import get_duration

def next_month(): return datetime.now()+relativedelta(months=+1)
class Capex(models.Model):
	'''данные о суммах капитальных расходов'''
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	variant_name = models.CharField('Название варианта',
                            max_length=255, default='Новый вариант')
	name = models.CharField('Название объекта',
                            max_length=255, default='Новый объект')
	amount_capital_expenditure = models.FloatField('Сумма капитальных расходов с НДС',
												validators=[MinValueValidator(1), ],
												default=1,)
	capex_without_VAT = models.FloatField('Сумма капитальных расходов без НДС',
												validators=[MinValueValidator(0), ],
												default=0,)
	VAT_rate = models.PositiveIntegerField('Ставка НДС с капитальных расходов',
								default=0,
								choices=choices.RATES,
								validators=[MinValueValidator(0), MaxValueValidator(100)],
                                )
	monthly_depreciation = models.FloatField('ежемесячная аммортизация',
												validators=[MinValueValidator(0), ],
												default=0,)
	annual_depreciation = models.FloatField('Годовая аммортизация',
												validators=[MinValueValidator(0), ],
												default=0,)
	monthly_tax_depreciation = models.FloatField('ежемесячная налоговая аммортизация',
												validators=[MinValueValidator(0), ],
												default=0,)
	annual_tax_depreciation = models.FloatField('Годовая налоговая аммортизация',
												validators=[MinValueValidator(0), ],
												default=0,)
	start_date = models.DateTimeField('Дата начала', default=datetime.now)
	end_date = models.DateTimeField('Дата окончания', default=next_month)
	VAT_refund = models.BooleanField('Планируется возмещение НДС из бюджета', 
									default=False,)
	leasing_switch = models.BooleanField('Объект будет в лизинге', default=False)
	VAT = models.FloatField('Сумма НДС с капитальных расходов',
							default=0,
							validators=[MinValueValidator(0), ],	
							blank=True, null=True)
	deprication_period = models.PositiveIntegerField('Срок амортизации, в месяцах', default=0,)
	liquidation_cost_switch = models.BooleanField('Включать в расчет амортизации ликвидационные расходы',
												default=False)
	liquidation_profit_switch = models.BooleanField('Вычитать из расчета амортизации доходы при реализации имущества в конце срока',
												default=False,)
	liquidation_cost = models.FloatField('Ликвидационные расходы с НДС',
										default=0,
                                        validators=[MinValueValidator(0), ],
                                        )
	liquidation_cost_VAT_rate = models.PositiveSmallIntegerField('Ставка НДС с лик. расходов',
								default=0,
								choices=choices.RATES,
								validators=[MinValueValidator(0), MaxValueValidator(100)],
                                )
	liquidation_profit = models.FloatField('Ожидаемая сумма от продажи в конце проекта с НДС',
                                            validators=[MinValueValidator(0), ],
                                            default=0,
                                        )
	liquidation_profit_VAT_rate = models.PositiveSmallIntegerField('Ставка НДС от суммы от продаж в конце проекта', default=0,
								validators=[MinValueValidator(0), MaxValueValidator(100)],
								choices=choices.RATES,
                                )
	taxdeprication_switch = models.BooleanField('Налоговая амортизация отличается от бухгалтерской',
                                                default=False,)
	taxdeprication_period = models.PositiveIntegerField('Срок амортизации для налогового учета, в месяцах',
                                                default=0,
                                                )
	amortization_premium = models.FloatField('Доля (в %) от стоимости основного средства в амортизационной премии для расчета налоговой амортизации',
												validators=[MinValueValidator(0), ],
                                                default=0,)

	def __str__(self):
		return self.name

	def duration(self):
		if self.start_date and self.end_date:
			return get_duration(self.start_date, self.end_date)
		else:
			return '0 лет 0 месяцев 0 дней'


class CapexObjectSetting(models.Model):
	'''доп. настройки об объекте капитальных расходов'''
	capex = models.OneToOneField(Capex, on_delete=models.CASCADE, related_name='object_settings')
	location = models.TextField('Данные локации',
								max_length=350,
                                blank=True, null=True)
	cadastral_number = models.TextField('Кадастровый номер',
										max_length=20,
                                        blank=True, null=True)
	square = models.FloatField('Площадь земельного участка',
                                validators=[MinValueValidator(0),],
								blank=True, null=True
                                )
	construction = models.TextField('Выполняемые СМР',
                                max_length=2000,
								blank=True, null=True)
	gcontractor = models.TextField('Генеральный подрядчик',
                                max_length=350,
								blank=True, null=True)
	create_date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.capex.name

	class Meta:
		ordering = ['create_date']

class CapexObjectFile(models.Model):
	_object = models.ForeignKey(CapexObjectSetting, on_delete=models.CASCADE, related_name='files')
	file = models.FileField(upload_to='project_capex_files/%Y/%m/%d/%H:%M:%S', )
	create_date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self._object.capex.name
