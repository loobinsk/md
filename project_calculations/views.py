import json
from datetime import date
from rest_framework.response import Response
from rest_framework.views import APIView

from .calc_funcs import profit_and_loss, flow_funds
from .calc_funcs import balance, results


from .models import Calculation, ResultFinancialAnalys, Balance, CashFlowPlan, ProfitAndLossPlan
from project_financing_sources.models import LeasingContract, Credit


class GetBasicCalcData(APIView):

	def get(self, request):
		ResultFinancialAnalys.objects.all().delete()
		Balance.objects.all().delete()
		CashFlowPlan.objects.all().delete()
		ProfitAndLossPlan.objects.all().delete()

		calc = Calculation.objects.all().first()
		PL = profit_and_loss.ProfitAndLossPlan(calc)
		FL = flow_funds.FlowFunds(calc)
		BL = balance.BalanceCalc(calc)
		RS = results.FinancialAnalysisResult(calc)
		PL.add_data_in_db()
		FL.add_data_in_db()
		BL.add_data_in_db()
		RS.add_data_in_db()
		return Response('Все отлично')

class GetBasicCalcData2(APIView):

	def get(self, request, pk):
		pk=int(pk)
		calc = Calculation.objects.all().first()
		bc = profit_and_loss.ProfitAndLossPlan(calc)
		ff = flow_funds.FlowFunds(calc)
		date = ff.get_change_working_capital(3)
		return Response(date)
		# dict_data = bc.get_profit_and_loss_plan(pk)

		# return Response(dict_data)

class GetFlowFunds(APIView):

	def get(self, request):
		calc = Calculation.objects.all().first()
		bc = flow_funds.FlowFunds(calc)
		for pk in bc.daterange:
			data = {}
			fl = CashFlowPlan()
			fl.EBITDA = bc.get_EBITDA(pk)
			fl.working_weight_change = bc.change_working_capital[pk]
			fl.income_tax = bc.get_income_tax(pk)
			fl.net_cash_flow_from_operations = bc.get_net_cash_flow_operating_activities(pk)
			fl.payment_capital_costs = bc.get_payment_capital_expenses(pk)
			fl.VAT_refund = bc.get_VAT_refund(pk)
			fl.payment_liquidation_expenses = bc.get_payment_liquidation_expenses(pk)
			fl.receipt_liquidation_proceeds = bc.get_receipt_liquidation_proceeds(pk)
			fl.net_cash_flow_from_investing_activities = bc.get_net_cash_flow_investing_activities(pk)
			fl.receipt_from_owners = bc.get_receipt_owners(pk)
			fl.credit_receipt = bc.get_credit_receipt(pk)
			fl.return_credits = bc.get_return_loans(pk)
			fl.loan_repayment = bc.get_interest_payment(pk)
			fl.interest_payment = bc.get_leasing_payment(pk)
			fl.net_cash_flow_from_financing_activities = bc.get_net_cash_flow_financing_activities(pk)
			fl.net_cash_flow = bc.get_net_cash_flow(pk)
			fl.cash_balance_beginning_period = bc.get_сash_balance_beginning_period(pk)
			fl.cash_balance_the_end_period = bc.get_cash_balance_end_period(pk)

			# data['ebitda']=bc.get_EBITDA(pk)
			# data['change_working_capital']=bc.change_working_capital[pk]
			# data['налог на прибыль']=bc.get_income_tax(pk)
			# data['чистый денежный поток по операционной деятельности']=bc.get_net_cash_flow_operating_activities(pk)
			# data['оплата капитальных расходов']=bc.get_payment_capital_expenses(pk)
			# data['get_VAT_refund']=bc.get_VAT_refund(pk)
			# data['get_payment_liquidation_expenses']=bc.get_payment_liquidation_expenses(pk)
			# data['get_receipt_liquidation_proceeds']=bc.get_receipt_liquidation_proceeds(pk)
			# data['get_net_cash_flow_investing_activities']=bc.get_net_cash_flow_investing_activities(pk)
			# data['get_receipt_owners']=bc.get_receipt_owners(pk)
			# data['get_credit_receipt']=bc.get_credit_receipt(pk)
			# data['get_return_loans']=bc.get_return_loans(pk)
			# data['get_interest_payment']=bc.get_interest_payment(pk)
			# data['get_leasing_payment']=bc.get_leasing_payment(pk)
			# data['get_net_cash_flow_financing_activities']=bc.get_net_cash_flow_financing_activities(pk)
			# data['get_net_cash_flow']=bc.get_net_cash_flow(pk)
			# data['get_сash_balance_beginning_period']=bc.get_сash_balance_beginning_period(pk)
			# data['get_cash_balance_end_period']=bc.get_cash_balance_end_period(pk)
			return Response(True)


