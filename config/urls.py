from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.urls import re_path
from rest_framework import permissions, authentication

from django.conf import settings
from django.conf.urls.static import static

from drf_yasg.views import get_schema_view # new
from drf_yasg import openapi 

schema_view = get_schema_view(
    openapi.Info(
        title="Viel API",
        default_version="v1",
        description="API",
        terms_of_service="",
        contact=openapi.Contact(email="emmanuelgmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=(authentication.BasicAuthentication,)
)



urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('logistics/',include("logistics.urls")),
    
]

