# Generated by Django 4.0.4 on 2022-07-23 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0019_remove_variant_name_remove_variant_project_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Variant',
        ),
    ]
