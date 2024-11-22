from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet)
router.register(r'vehicles', VehicleViewSet)
router.register(r'jobs', JobViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('shipments/<str:tracking_id>/', ShipmentDetailView.as_view(), name='shipment'),
    path('shipments/', ShipmentCreateView.as_view(), name='shipment_create'),
    path('inventory/<str:warehouse_id>/', InventoryListView.as_view(), name='inventory_list'),
    path('optimize-routes/', RouteOptimizationView.as_view(), name='optimize_routes'),
    path('assign-driver/', AssignDriverView.as_view(), name='assign_driver'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
     path('api/signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]


