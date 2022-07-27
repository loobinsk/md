from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

from projects.models import Project
from projects import choices


class TaxPrmTemplate(models.Model):
	'''базовые параметры расчетов налогов'''
	VAT_standart_rate = models.FloatField('НДС (стандартная ставка), %',
							blank=True, null=True,
							default=0,
                            )
	VAT_preferential_rate = models.FloatField('НДС (льготная ставка), %',
							blank=True, null=True,
							default=0,
                            )
	VAT_export_rate = models.FloatField('НДС (экспортная ставка), %',
							blank=True, null=True,
							default=0,
                            )
	income_tax = models.FloatField('Налог на прибыль, %',
							blank=True, null=True,
							default=0,
                            )
	Social_tax = models.FloatField('Социальный налог, %',
							blank=True, null=True,
							default=0,
                            )

	def __str__(self):
		return 'базовые параметры налогов'

class get_tax_prm():
	try:
		tax_prm_template=TaxPrmTemplate.objects.first()
	except:
		tax_prm_template = None
	if tax_prm_template:
		VAT_standart_rate = tax_prm_template.VAT_standart_rate
		VAT_preferential_rate = tax_prm_template.VAT_preferential_rate
		VAT_export_rate = tax_prm_template.VAT_export_rate
		income_tax = tax_prm_template.income_tax
		Social_tax = tax_prm_template.Social_tax
	else:
		VAT_standart_rate = 0
		VAT_preferential_rate =0 
		VAT_export_rate=0
		income_tax = 0
		Social_tax = 0

class TaxPrm(models.Model):
	'''Ставки налогов при стандартном моделировании'''
	variant_name = models.CharField(max_length=255, default='Новый вариант')
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	tax_simulation = models.PositiveSmallIntegerField('моделирование налогов', choices=choices.TAX_SIMULATION, default=0)
	tax_min_burden = models.FloatField('Налоговая нагрузка',
										validators=[MinValueValidator(0), MaxValueValidator(100)],
										blank=True, null=True
                                        )
	tax_min_burden_base = models.PositiveSmallIntegerField('База для расчета налога', choices=choices.TAX_MIN_BURDEN_BASE,
															blank=True, null=True)
	calculation_frequency = models.PositiveSmallIntegerField('Частота расчета', choices=choices.TIME_DETALIZATIONS,
															blank=True, null=True)
	vat_standart_rate = models.FloatField('НДС (стандартная ставка), %',
							blank=True, null=True,
							default=get_tax_prm().VAT_standart_rate
                            )
	vat_preferential_rate = models.FloatField('НДС (льготная ставка), %',
							blank=True, null=True,
							default=get_tax_prm().VAT_preferential_rate
                            )
	vat_export_rate = models.FloatField('НДС (экспортная ставка), %',
							blank=True, null=True,
							default=get_tax_prm().VAT_export_rate
                            )
	income_tax = models.FloatField('Налог на прибыль, %',
							blank=True, null=True,
							default=get_tax_prm().income_tax
                            )
	social_tax = models.FloatField('Социальный налог, %',
							blank=True, null=True,
							default=get_tax_prm.Social_tax
                            )
	summ_ndpi = models.FloatField('Сумма НДПИ', blank=True, null=True)
	multiplier_ndpi = models.FloatField('Налоговый мультипликатор НДПИ', blank=True, null=True)
	allowance_ndpi = models.FloatField('Налоговая надбавка НДПИ', blank=True, null=True)
	summ_excise = models.FloatField('Сумма акциза', blank=True, null=True)
	multiplier_excise = models.FloatField('Налоговый мультипликатор акциза', blank=True, null=True)
	allowance_excise = models.FloatField('Налоговая надбавка акциза', blank=True, null=True)

	def __str__(self):
		return self.variant_name

	def get_variant_name(self):
		return self.variant_name


class DiscountRate(models.Model):
	'''Ставки дисконтирования'''
	variant_name = models.CharField(max_length=255, default='Новый вариант')
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	discount_rate_general_install = models.FloatField('Установленная ставка дисконтирования, % (общая для всех лет)',
									validators=[MinValueValidator(0), MaxValueValidator(100)],
									default=0)
	reinvesting_rate = models.FloatField('Ставка реинвестирования, %',
									validators=[MinValueValidator(0), MaxValueValidator(100)],
									default=0,)
	def __str__(self):
		return self.variant_name