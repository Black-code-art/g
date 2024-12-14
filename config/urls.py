from django.contrib import admin
from django.urls import path,include
from django.http import JsonResponse
from django.urls import re_path
from rest_framework import permissions,authentication
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.http import HttpResponseRedirect


def redirect_to_swagger(request):
    return HttpResponseRedirect('/swagger/')

def welcome(request):
    return JsonResponse(
        {
            "message": "Welcome to Veil logistics",
            "status": 200,
        }
    )
schema_view = get_schema_view(
   openapi.Info(
      title="VEIL LOGISTICS",
      default_version='v1',
      description="API",
      terms_of_service="",
      contact=openapi.Contact(email="emmanuelebube117@gmail.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
   authentication_classes= (authentication.BasicAuthentication,)
)



urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('', redirect_to_swagger), 
    path('logistics/',include("logistics.urls")),
    
]

