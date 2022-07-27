# Generated by Django 4.0.4 on 2022-07-07 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0013_alter_additionalprojectinformation_contract_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variant',
            name='user',
        ),
        migrations.AlterField(
            model_name='projectfile',
            name='file_type',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Основной'), (1, 'Дополнительный')], default=0, verbose_name='Тип файла'),
        ),
    ]
