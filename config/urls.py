from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView
from drf_spectacular.views import SpectacularSwaggerView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/projects/', include('projects.urls')),
    path('api/project_taxes/', include('project_taxes.urls')),
    path('api/economic_indicators/', include('project_economic_indicators.urls')),
    path('api/sales/', include('project_sales.urls')),
    path('api/financing_sources/', include('project_financing_sources.urls')),
    path('api/project_calculations/', include('project_calculations.urls')),
    path('api/account/', include('account.urls')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
