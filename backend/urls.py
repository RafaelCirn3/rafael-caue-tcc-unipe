from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema')),
    path('api/v1/auth/', include('apps.accounts.urls')),
    path('api/v1/users/', include('apps.accounts.user_urls')),
    path('api/v1/', include('apps.financial_aux.urls')),
    path('api/v1/education/', include('apps.education.urls')),
    path('api/v1/simulations/', include('apps.simulations.urls')),
    path('admin/', admin.site.urls),
]
