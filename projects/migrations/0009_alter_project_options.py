# Generated by Django 4.0.4 on 2022-06-22 06:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_alter_variant_table'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-create_date']},
        ),
    ]
