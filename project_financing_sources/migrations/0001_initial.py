# Generated by Django 4.0.4 on 2022-07-23 12:07

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
            name='WorkingCapitalParameter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variant_name', models.CharField(default='Новый вариант', max_length=255)),
                ('share_deferred_sales_general', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Доля продаж с отсрочкой, %')),
                ('percentage_immediate_pay_sales', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Доля продаж с незамедлительной оплатой')),
                ('share_purchases_with_immediate_payment', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Доля закупок с незамедлительной оплатой ')),
                ('share_advance_sales_general', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Доля продаж с авансами, %')),
                ('turnover_deferred_sales_general', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Средний срок отсрочки по продажам, дней')),
                ('turnover_advance_sales_general', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Средний срок авансов от продаж, дней')),
                ('share_different_purchase_general', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Доля закупок с отсрочкой платежа, %')),
                ('share_advance_purchase_general', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Доля закупок с авансовыми платежами, %')),
                ('turnover_different_purchase_general', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Средний срок оплаты поставок, дней')),
                ('turnover_advance_purchase_general', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Срок авансов по закупкам, дней')),
                ('turnover_inventory_general', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Срок оборачиваемости запасов, дней')),
                ('turnover_vat_general', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Средний срок остатков НДС по приобретенным ценностям (отложенного НДС), в днях')),
                ('share_cash_sales_general', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Доля продаж с немедленной оплатой, %')),
                ('wc_end_switch', models.BooleanField(default=False, verbose_name='Списывать рабочий капитал в конце проекта')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания записи')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
            ],
        ),
        migrations.CreateModel(
            name='OwnFundVariant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variant_name', models.CharField(default='Новый вариант', max_length=255)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
            ],
        ),
        migrations.CreateModel(
            name='OwnFund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_sum', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Сумма вложений')),
                ('name', models.CharField(default='Новый взнос', max_length=255)),
                ('source_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата вложения собственных средств')),
                ('source_investor', models.CharField(blank=True, max_length=255, null=True, verbose_name='Инвестор')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='own_funds', to='project_financing_sources.ownfundvariant')),
            ],
        ),
        migrations.CreateModel(
            name='LeasingContractVariant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variant_name', models.CharField(default='Новый вариант', max_length=255)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
            ],
        ),
        migrations.CreateModel(
            name='LeasingContract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lessor', models.TextField(blank=True, max_length=350, null=True, verbose_name='Лизингодатель')),
                ('name', models.CharField(default='Лизинговая операция', max_length=255)),
                ('object_cost', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Стоимость объекта')),
                ('date_planned_accounting_object', models.DateTimeField(blank=True, null=True, verbose_name='Дата планового учета объекта')),
                ('initial_payment', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Доля первоначального взноса')),
                ('contract_start_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата договора')),
                ('term_leasing_contract', models.PositiveIntegerField(default=0, verbose_name='Срок лизингового договора, мес')),
                ('monthly_lease_payment', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Ежемесячные лизинговые платежи (с НДС), руб')),
                ('redemption_sum_general', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Сумма выкупного платежа')),
                ('VAT_rate', models.PositiveSmallIntegerField(choices=[(0, 'Не облагается'), (1, '0'), (2, '10'), (3, '20')], default=0, verbose_name='Ставка ндс')),
                ('distribution_redemption_switch', models.BooleanField(default=False, verbose_name='Распределение выкупного платежа по периодам')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leasings', to='project_financing_sources.leasingcontractvariant')),
            ],
        ),
        migrations.CreateModel(
            name='CreditVariant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variant_name', models.CharField(default='Новый вариант', max_length=255)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
            ],
        ),
        migrations.CreateModel(
            name='Credit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Новый кредит', max_length=255)),
                ('lender', models.TextField(blank=True, max_length=350, null=True, verbose_name='Банк')),
                ('date', models.DateTimeField(blank=True, null=True, verbose_name='Дата договора')),
                ('sum_in_currancy', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Сумма')),
                ('date_in', models.DateTimeField(blank=True, null=True, verbose_name='Дата получения')),
                ('capitalization', models.BooleanField(default=False, verbose_name='Капитализация процентов')),
                ('interest_rate', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Процентная ставка, %')),
                ('tenor', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Срок займа, мес.')),
                ('calculation_type', models.PositiveSmallIntegerField(choices=[(0, 'Дифференцируемый'), (1, 'Аннуитетный')], default=0, verbose_name='Тип уплаты')),
                ('grace_period_principal', models.PositiveIntegerField(default=0, verbose_name='Грейс-период основного платежа, в мес.')),
                ('grace_period_interest', models.PositiveIntegerField(default=0, verbose_name='Грейс-период процентных платежей, в мес.')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credits', to='project_financing_sources.creditvariant')),
            ],
        ),
    ]
