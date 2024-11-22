from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status


class SignupView(generics.CreateAPIView):
    serializer_class = UserSignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": {
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role
            }
        }, status=status.HTTP_201_CREATED)

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class =JobSerializer

class ShipmentDetailView(generics.RetrieveAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    lookup_field = 'tracking_id'


class ShipmentCreateView(generics.CreateAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer


class InventoryListView(generics.ListAPIView):
    serializer_class = InventorySerializer
    def get_queryset(self):
        warehouse_id = self.kwargs['warehouse_id']
        return Inventory,object,filter(warehouse_id = warehouse_id)

class RouteOptimizationView(generics.CreateAPIView):
    queryset = RouteOptimization.objects.all()
    serializer_class = RouteOptimizationSerializer
    
class AssignDriverView(generics.UpdateAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer

class SomeProtectedView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response({"message": "This is a protected view!"})
    
User  = get_user_model()

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

class LogoutView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            token = request.data["refresh"]
            token_obj = RefreshToken(token)
            token_obj.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)