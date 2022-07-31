# Generated by Django 4.0.4 on 2022-07-28 18:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_economic_indicators', '0004_remove_capex_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='capex',
            name='liquidation_cost_VAT_rate',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Не облагается'), (1, '0'), (2, '10'), (3, '20')], default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Ставка НДС с лик. расходов'),
        ),
        migrations.AlterField(
            model_name='capex',
            name='liquidation_profit_VAT_rate',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Не облагается'), (1, '0'), (2, '10'), (3, '20')], default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Ставка НДС от суммы от продаж в конце проекта'),
        ),
    ]
