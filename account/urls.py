from django.urls import path
from . import views

urlpatterns = [
	path('register/',
		views.RegisterUserView.as_view(),
		name='register'),
	path('login/',
		views.LoginAPIView.as_view(),
		name='auth'),
	path('me/', views.UserMeView.as_view(), name='get_user_me')
]
