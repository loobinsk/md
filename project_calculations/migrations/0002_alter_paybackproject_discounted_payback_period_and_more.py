# Generated by Django 4.0.4 on 2022-08-09 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_calculations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paybackproject',
            name='discounted_payback_period',
            field=models.TextField(blank=True, null=True, verbose_name='Дисконтированный срок окупаемости'),
        ),
        migrations.AlterField(
            model_name='paybackproject',
            name='nominal_payback_period',
            field=models.TextField(blank=True, null=True, verbose_name='Номинальный срок окупаемости'),
        ),
    ]