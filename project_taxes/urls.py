from django.urls import path
from . import views

urlpatterns = [
	path('tax_prms/enums/',
		views.TaxPrmEnums.as_view(),
		name='tax_prm_enums'
		),
	path('tax_prms/',
		views.TaxPrmListView.as_view(),
		name='tax_prm_list'
		),
	path('tax_prms/<pk>/',
		views.TaxPrmGetUpdateView.as_view(),
		name='tax_prm_get_or_update'),
	path('tax_prms/copy/<pk>/',
		views.CopyTaxPrm.as_view(),
		name='tax_prm_get_or_update'),
	
	path('discount_rates/',
		views.DiscountRateCreateListView.as_view(),
		name='discount_rate_list'),
	path('discount_rates/<pk>/',
		views.DiscountRateGetUpdateView.as_view(),
		name='discount_rate_detail'),
	path('discount_rates/copy/<pk>/',
		views.DiscountRateCopyView.as_view(),
		name='discount_rate_copy'),
]
