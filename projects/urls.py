from django.urls import path
from . import views

urlpatterns = [

	path('create_new_project/',
		views.CreateNewProject.as_view(),
		name='create_new_project'),
	path('project_update/<pk>/',
		views.ProjectUpdate.as_view(),
		name='projects_update'),
	path('get_projects/',
		views.GetProjectsView.as_view(),
		name='get_projects'),
	path('project_file_get_or_create/',
		views.FileCreateView.as_view(),
		name='project_file_create'),
	path('project_file_del/<pk>/',
		views.FileDeleteView.as_view(),
		name='project_file_del'),

	path('additional_project_information_update/<pk>/',
		views.AdditionalProjectInformationUpdate.as_view(),
		name='additional_project_information_update'),
	path('copied_project_update/<pk>/',
		views.CopiedProjectUpdate.as_view(),
		name='copied_project_update'),
	path('project_company_update/<pk>/',
		views.ProjectCompanyUpdate.as_view(),
		name='project_company_update'),
	path('get_projects_enums/',
		views.GetProjectsEnumsView.as_view(),
		name='get_projects_enums'),
	path('get_project_name/<pk>/',
		views.GetProjectNameView.as_view(),
		name='get_project_name'),
]
