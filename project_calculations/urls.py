from django.urls import path
from . import views

urlpatterns = [
	path('test/', views.TestView.as_view()),	

	path('calculations/enums/<pk>/', views.CalculationEnums.as_view()),
	path('calculations/<pk>/', views.CalculationView.as_view()),
	path('calculation_results/<pk>/', views.CalcResultsView.as_view()),
	path('profit_and_loss_plan_data/<pk>/', views.ProfitAndLossPlanView.as_view()),
	path('cash_flow_plan_data/<pk>/', views.CashFlowPlanView.as_view()),
	path('balance_data/<pk>/', views.BalanceView.as_view()),
	path('result_fin_analys_data/<pk>/', views.ResultFinancialAnalysView.as_view()),

]
