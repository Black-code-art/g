from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'shipments', ShipmentViewSet)


urlpatterns = [
    path('', include(router.urls)),
 
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('price/<uuid:shipment_id>/', CalculatePrice.as_view()),
    path('assign_driver/<uuid:shipment_id>/<uuid:driver_id>/', AssignDriver.as_view())
]


