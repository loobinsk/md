from django.urls import path
from . import views

urlpatterns = [
	path('capexs/enums/',
		views.CapexEnums.as_view(),
		name='capex_object_file_detail'),
	path('capexs/',
		views.CapexListView.as_view(),
		name='capex_list'),
	path('capexs/<pk>/',
		views.CapexDetailView.as_view(),
		name='capex_detail'),
	path('capexs/copy/<pk>/',
		views.CopyCapexView.as_view(),
		name='capex_copy'),
	path('capex_object_settings/<pk>/',
		views.CapexObjectDetailView.as_view(),
		name='capex_object_settings'),
	path('capex_object_files/',
		views.CapexObjectFileListView.as_view(),
		name='capex_object_files'),
	path('capex_object_files/<pk>/',
		views.CapexObjectFileDetailView.as_view(),
		name='capex_object_file_detail'),
]
