from django.urls import path
from . import views

urlpatterns = [
	path('test/', views.GetBasicCalcData.as_view()),
]
