from django.contrib import admin
from . import models


admin.site.register(models.Calculation)
admin.site.register(models.MainParameter)
admin.site.register(models.FundingAmount)
admin.site.register(models.AnnualAverage)
admin.site.register(models.BasicIndicator)
admin.site.register(models.PaybackProject)
admin.site.register(models.Rating)



class ProfitAndLossPlanAdmin(admin.ModelAdmin):
	list_display = [
		'calculation', 
		'month', 
		'revenue', 
		'сost_price', 
		'gross_profit', 
		'business_expenses', 
		'management_expenses', 
		'operating_income_ebit',
		'interest_expenses',
		'profit_before_tax',
		'income_tax',
		'net_profit',
		'ebitda']
	list_filter = ['calculation', 'month']

admin.site.register(models.ProfitAndLossPlan, ProfitAndLossPlanAdmin)

class CashFlowPlanAdmin(admin.ModelAdmin):
	list_display = [
		'calculation', 
		'month', 
		'EBITDA', 
		'working_weight_change', 
		'income_tax', 
		'net_cash_flow_from_operations', 
		'payment_capital_costs', 
		'VAT_refund', 
		'payment_liquidation_expenses', 
		'receipt_liquidation_proceeds',
		'net_cash_flow_from_investing_activities',
		'receipt_from_owners',
		'credit_receipt',
		'return_credits',
		'loan_repayment',
		'interest_payment',
		'net_cash_flow_from_financing_activities',
		'net_cash_flow',
		'cash_balance_beginning_period',
		'cash_balance_the_end_period',]
	list_filter = ['calculation', 'month']

admin.site.register(models.CashFlowPlan, CashFlowPlanAdmin)

class BalanceAdmin(admin.ModelAdmin):
	list_display = [
		'calculation', 
		'month', 
		'fixed_assets', 
		'Total_non_current_assets', 
		'Stocks', 
		'accounts_receivable', 
		'cash', 
		'total_current_assets', 
		'total_balance', 
		'authorized_share_capital',
		'undestributed_profits',
		'total_equity',
		'borrowed_funds',
		'accounts_payable',
		'total_liabilities',
		'Total_balance2',]
	list_filter = ['calculation', 'month']

admin.site.register(models.Balance, BalanceAdmin)

class ResultFinancialAnalysAdmin(admin.ModelAdmin):
	list_display = [
		'calculation', 
		'month', 
		'return_on_sales_rot', 
		'return_on_equity_roe', 
		'return_on_assets_roa', 
		'asset_turnover_ratio', 
		'сurrent_assets_turnover_ratio', 
		'inventory_turnover_ratio', 
		'accounts_receivable_turnover_ratio', 
		'accounts_payable_turnover_ratio',
		'autonomy_coefficient',
		'leverage_ratio_de',
		'own_working_capital_ratio',
		'absolute_liquidity_ratio',
		'interim_liquidity_ratio',
		'current_liquidity_ratio',]
	list_filter = ['calculation', 'month']

admin.site.register(models.ResultFinancialAnalys, ResultFinancialAnalysAdmin)