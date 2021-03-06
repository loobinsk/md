# Generated by Django 4.0.4 on 2022-07-08 18:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0017_alter_variant_name_alter_variant_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variant',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='projects.project'),
        ),
    ]
