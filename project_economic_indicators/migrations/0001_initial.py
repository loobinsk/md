# Generated by Django 4.0.4 on 2022-07-23 12:07

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0020_delete_variant'),
    ]

    operations = [
        migrations.CreateModel(
            name='Capex',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variant_name', models.CharField(default='Новый вариант', max_length=255, verbose_name='Название варианта')),
                ('name', models.CharField(default='Новый объект', max_length=255, verbose_name='Название объекта')),
                ('amount_capital_expenditure', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Сумма капитальных расходов с НДС')),
                ('capex_without_VAT', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Сумма капитальных расходов без НДС')),
                ('VAT_rate', models.PositiveIntegerField(choices=[(0, 'Не облагается'), (1, '0'), (2, '10'), (3, '20')], default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Ставка НДС с капитальных расходов')),
                ('monthly_depreciation', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='ежемесячная аммортизация')),
                ('annual_depreciation', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Годовая аммортизация')),
                ('monthly_tax_depreciation', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='ежемесячная налоговая аммортизация')),
                ('annual_tax_depreciation', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Годовая налоговая аммортизация')),
                ('start_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата начала')),
                ('end_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата окончания')),
                ('duration', models.CharField(blank=True, default='0 лет 0 месяцев 0 дней', max_length=255, null=True, verbose_name='Длительность проекта')),
                ('VAT_refund', models.BooleanField(default=False, verbose_name='Планируется возмещение НДС из бюджета')),
                ('leasing_switch', models.BooleanField(default=False, verbose_name='Объект будет в лизинге')),
                ('VAT', models.FloatField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Сумма НДС с капитальных расходов')),
                ('deprication_period', models.PositiveIntegerField(default=0, verbose_name='Срок амортизации, в месяцах')),
                ('liquidation_cost_switch', models.BooleanField(default=False, verbose_name='Включать в расчет амортизации ликвидационные расходы')),
                ('liquidation_profit_switch', models.BooleanField(default=False, verbose_name='Вычитать из расчета амортизации доходы при реализации имущества в конце срока')),
                ('liquidation_cost', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Ликвидационные расходы с НДС')),
                ('liquidation_cost_VAT_rate', models.FloatField(choices=[(0, 'Не облагается'), (1, '0'), (2, '10'), (3, '20')], default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Ставка НДС с лик. расходов')),
                ('liquidation_profit', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Ожидаемая сумма от продажи в конце проекта с НДС')),
                ('liquidation_profit_VAT_rate', models.FloatField(choices=[(0, 'Не облагается'), (1, '0'), (2, '10'), (3, '20')], default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Ставка НДС от суммы от продаж в конце проекта')),
                ('taxdeprication_switch', models.BooleanField(default=False, verbose_name='Налоговая амортизация отличается от бухгалтерской')),
                ('taxdeprication_period', models.PositiveIntegerField(default=0, verbose_name='Срок амортизации для налогового учета, в месяцах')),
                ('amortization_premium', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Доля (в %) от стоимости основного средства в амортизационной премии для расчета налоговой амортизации')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
            ],
        ),
        migrations.CreateModel(
            name='CapexObjectSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.TextField(blank=True, max_length=350, null=True, verbose_name='Данные локации')),
                ('cadastral_number', models.TextField(blank=True, max_length=20, null=True, verbose_name='Кадастровый номер')),
                ('square', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Площадь земельного участка')),
                ('construction', models.TextField(blank=True, max_length=2000, null=True, verbose_name='Выполняемые СМР')),
                ('gcontractor', models.TextField(blank=True, max_length=350, null=True, verbose_name='Генеральный подрядчик')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('capex', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='object_settings', to='project_economic_indicators.capex')),
            ],
            options={
                'ordering': ['create_date'],
            },
        ),
        migrations.CreateModel(
            name='CapexObjectFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='project_capex_files/%Y/%m/%d/%H:%M:%S')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='project_economic_indicators.capexobjectsetting')),
            ],
        ),
    ]
