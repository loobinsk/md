# Generated by Django 4.0.4 on 2022-08-02 09:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_calculations', '0004_alter_balance_month_alter_cashflowplan_month_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField(verbose_name='Рейтинг проекта')),
                ('comment', models.TextField(verbose_name='Комментарий к рейтингу')),
            ],
        ),
        migrations.RemoveField(
            model_name='mainparameter',
            name='rating',
        ),
        migrations.AlterField(
            model_name='annualaverage',
            name='calculation',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='annual_average', to='project_calculations.calculation'),
        ),
        migrations.AlterField(
            model_name='basicindicator',
            name='calculation',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='basic_indicators', to='project_calculations.calculation'),
        ),
        migrations.AlterField(
            model_name='fundingamount',
            name='calculation',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='funding_amounts', to='project_calculations.calculation'),
        ),
        migrations.AlterField(
            model_name='mainparameter',
            name='calculation',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='main_parameters', to='project_calculations.calculation'),
        ),
        migrations.AlterField(
            model_name='paybackproject',
            name='calculation',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payback_project', to='project_calculations.calculation'),
        ),
    ]