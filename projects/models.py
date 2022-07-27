from django.db import models
from account.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from . import choices


class Currency(models.Model):
	'''валюты'''
	name = models.CharField(max_length=255)
	name_en = models.CharField(max_length=255)

	def __str__(self):
		return self.name

class Country(models.Model):
	'''список стран с их валютами'''
	name = models.CharField(max_length=255)
	name_en = models.CharField(max_length=255)
	code = models.CharField(max_length=20)
	prefix = models.CharField(max_length=20)
	currency = models.ForeignKey(Currency, on_delete=models.PROTECT)

	def __str__(self):
		return f'{self.name}'

class Industry(models.Model):
	'''список экономических отраслей и соответствующие им сегменты.'''
	name = models.TextField(max_length=255)
	name_en = models.TextField(max_length=255, blank=True, null=True)

	def __str__(self):
		return f'{self.name}'

class Segment(models.Model):
	industry = models.ForeignKey(Industry, on_delete=models.CASCADE)
	name = models.TextField(max_length=255)
	name_en = models.TextField(max_length=255, blank=True, null=True)

	def __str__(self):
		return f'{self.name}'

class Project(models.Model):
	'''Основная модель системы - паспорт проекта'''
	name = models.CharField('Короткое название проекта',
							max_length=255, default='Новый проект')
	financing_type = models.PositiveSmallIntegerField('Тип проекта', 
									choices=choices.FINANCING_TYPE, null=True, default=0)
	industry_main = models.ForeignKey(Industry, 
									on_delete=models.PROTECT,
									related_name='industry_main', blank=True, null=True)
	industry_segments = models.ManyToManyField(Segment, blank=True)
	currency = models.ForeignKey(Currency, on_delete=models.PROTECT,
								verbose_name='Валюта проекта', blank=True, null=True)
	currency_multiplication = models.PositiveSmallIntegerField('Мультипликатор денежного измерения',
														choices=choices.CURRENCY_MULTIPLICATION, default=0)
	time_detalization = models.PositiveSmallIntegerField('Детализация проекта',
														choices=choices.TIME_DETALIZATIONS,
                                                        default=0,
                                                        )
	fin_source_equity = models.BooleanField('Использование собственного капитала в проекте',
											default=True,)
	fin_source_credit = models.BooleanField('Использование банковского кредита в проекте',
											default=False,)
	fin_source_leasing = models.BooleanField('Использование лизинга (финансовой аренды) в проекте',
											default=False,)
	comments = models.TextField(blank=True, null=True)
	create_date = models.DateTimeField('Дата создания записи', auto_now_add=True)
	update_date = models.DateTimeField('Дата обновления проекта',auto_now=True)
	author = models.ForeignKey(User, 
								verbose_name='Автор проекта',
								related_name='author',
								on_delete=models.CASCADE)
	active = models.BooleanField('Проект активен', default=True)
	
	class Meta:
		ordering = ['-create_date']

	def __init__(self, *args, **kwargs):
		super(Project, self).__init__(*args, **kwargs)
		self.init_industry_main = self.industry_main

	def __str__(self):
		return f'{self.name}'


class AdditionalProjectInformation(models.Model):
	project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='additional_project_information')
	name_full = models.TextField('Полное название проекта',
							max_length=300,blank=True, null=True)
	country = models.ForeignKey(Country, on_delete=models.PROTECT,
								verbose_name='Страна',
								blank=True, null=True)
	user_code = models.CharField('Пользовательский (внутренний) код проекта',
							max_length=20,
                            blank=True, null=True)
	init_date = models.DateTimeField('Дата инициализации проекта',
								blank=True, null=True
                                )
	contract = models.CharField('Номер инвестиционного контракта',
                            max_length=20,
                            blank=True, null=True)
	contract_date = models.DateTimeField('Дата инвестиционного контракта',
                            blank=True, null=True)
	full_name_person_responsible = models.CharField(max_length=255, 
													blank=True, null=True)

	def __str__(self):
		return self.name_full

class CopiedProject(models.Model):
	'''настройки типового проекта'''
	project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='copy_project')
	copied_project = models.BooleanField('Проект является типовым', default=False)
	name = models.CharField('Название типового проекта', 
                            max_length=255,blank=True, null=True)
	ext_switch = models.BooleanField('Доступ типового проекта другим пользователям организации',
									default=False,
									blank=True, null=True)
	finance_switch = models.BooleanField('Сохранять финансовые данные в типовом проекте',
											default=False,
											blank=True, null=True)
	def __str__(self):
		return f'{self.name}'

class ProjectCompany(models.Model):
	'''Планируемая компания для проекта'''
	project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_company')
	date_init = models.DateTimeField('Планируемая дата регистрации предприятия',
								blank=True, null=True
                                )
	name = models.CharField('Рабочее название предприятия', 
							max_length=255)
	company_sme = models.BooleanField('Предприятие относится к разряду малого и среднего бизнеса',
									blank=True, null=True)
                            
	def __str__(self):
		return f'{self.name}'

class ProjectFile(models.Model):
	'''файлы проекта'''
	project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_files')
	file = models.FileField(upload_to='project_files/%Y/%m/%d/%H:%M:%S')
	file_type = models.PositiveSmallIntegerField('Тип файла',
								choices=choices.FILE_TYPES, default=0,                                     
                                )

class ProjectTemplate(models.Model):
	'''Проект, который является шаблоном для создания проекта.'''
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	name = models.CharField(max_length=255, blank=True, null=True)
	create_date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name




















	















	