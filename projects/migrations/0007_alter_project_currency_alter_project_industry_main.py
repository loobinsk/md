# Generated by Django 4.0.4 on 2022-06-17 13:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_alter_project_currency_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='projects.currency', verbose_name='Валюта проекта'),
        ),
        migrations.AlterField(
            model_name='project',
            name='industry_main',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='industry_main', to='projects.industry'),
        ),
    ]
