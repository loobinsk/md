# Generated by Django 4.0.4 on 2022-07-28 18:21

from django.db import migrations, models
import django.utils.timezone
import project_economic_indicators.models


class Migration(migrations.Migration):

    dependencies = [
        ('project_economic_indicators', '0002_alter_capex_amount_capital_expenditure_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='capex',
            name='end_date',
            field=models.DateTimeField(default=project_economic_indicators.models.next_month, verbose_name='Дата окончания'),
        ),
        migrations.AlterField(
            model_name='capex',
            name='start_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата начала'),
        ),
    ]