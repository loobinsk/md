# Generated by Django 4.0.4 on 2022-07-23 12:11

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
            name='TaxPrmTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('VAT_standart_rate', models.FloatField(blank=True, default=0, null=True, verbose_name='НДС (стандартная ставка), %')),
                ('VAT_preferential_rate', models.FloatField(blank=True, default=0, null=True, verbose_name='НДС (льготная ставка), %')),
                ('VAT_export_rate', models.FloatField(blank=True, default=0, null=True, verbose_name='НДС (экспортная ставка), %')),
                ('income_tax', models.FloatField(blank=True, default=0, null=True, verbose_name='Налог на прибыль, %')),
                ('Social_tax', models.FloatField(blank=True, default=0, null=True, verbose_name='Социальный налог, %')),
            ],
        ),
        migrations.CreateModel(
            name='TaxPrm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variant_name', models.CharField(default='Новый вариант', max_length=255)),
                ('tax_simulation', models.PositiveSmallIntegerField(choices=[(0, 'минимальное'), (1, 'стандартное')], default=0, verbose_name='моделирование налогов')),
                ('tax_min_burden', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Налоговая нагрузка при планировании MIN')),
                ('tax_min_burden_base', models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Выручка'), (1, 'Прибыль до налогообложения')], null=True, verbose_name='База для расчета налога')),
                ('calculation_frequency', models.PositiveSmallIntegerField(blank=True, choices=[(0, 'По годам'), (1, 'По кварталам'), (2, 'По месяцам'), (3, 'По полугодиям')], null=True, verbose_name='Частота расчета')),
                ('vat_standart_rate', models.FloatField(blank=True, default=0, null=True, verbose_name='НДС (стандартная ставка), %')),
                ('vat_preferential_rate', models.FloatField(blank=True, default=0, null=True, verbose_name='НДС (льготная ставка), %')),
                ('vat_export_rate', models.FloatField(blank=True, default=0, null=True, verbose_name='НДС (экспортная ставка), %')),
                ('income_tax', models.FloatField(blank=True, default=0, null=True, verbose_name='Налог на прибыль, %')),
                ('social_tax', models.FloatField(blank=True, default=0, null=True, verbose_name='Социальный налог, %')),
                ('summ_ndpi', models.FloatField(blank=True, null=True, verbose_name='Сумма НДПИ')),
                ('multiplier_ndpi', models.FloatField(blank=True, null=True, verbose_name='Налоговый мультипликатор НДПИ')),
                ('allowance_ndpi', models.FloatField(blank=True, null=True, verbose_name='Налоговая надбавка НДПИ')),
                ('summ_excise', models.FloatField(blank=True, null=True, verbose_name='Сумма акциза')),
                ('multiplier_excise', models.FloatField(blank=True, null=True, verbose_name='Налоговый мультипликатор акциза')),
                ('allowance_excise', models.FloatField(blank=True, null=True, verbose_name='Налоговая надбавка акциза')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
            ],
        ),
        migrations.CreateModel(
            name='DiscountRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variant_name', models.CharField(default='Новый вариант', max_length=255)),
                ('discount_rate_general_install', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Установленная ставка дисконтирования, % (общая для всех лет)')),
                ('reinvesting_rate', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Ставка реинвестирования, %')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
            ],
        ),
    ]