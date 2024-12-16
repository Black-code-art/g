from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication 
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .logistics import generate_tracking_id
from .permissions import IsAdmin




class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer



    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):

        serializer = UserSerializer(self.queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
       



class ShipmentViewSet(viewsets.ModelViewSet):


    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]




    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.validated_data['customer'] = request.user
        serializer.validated_data['status'] = 'Pending'
        serializer.validated_data['tracking_id'] = generate_tracking_id()

        self.perform_create(serializer)


        return Response(serializer.data, status=status.HTTP_201_CREATED)




class CalculatePrice(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, shipment_id):

        try:
            shipment = Shipment.objects.get(id=shipment_id)

        except Shipment.DoesNotExist:
            return Response({"message": "Shipment not found"}, status=status.HTTP_404_NOT_FOUND)
        
        weight = shipment.weight

        if weight < 10:
            price = 1000

        elif weight < 20:
            price = 2000


        elif weight < 30:
            price = 3000
        
        else:
            price = 8000



        return Response(
            {
                "price": price,
                "tracking_id": shipment.tracking_id,
                "weight": shipment.weight

            }, 
            status=200
        )


      
class AssignDriver(APIView):

    permission_classes = [IsAdmin]
    authentication_classes = [JWTAuthentication]

    def post(self, request, shipment_id, driver_id):

        try:
            shipment = Shipment.objects.get(id=shipment_id)
            driver = User.objects.get(id=driver_id)

        except User.DoesNotExist:
            return Response({"message": "Driver not found"}, status=status.HTTP_404_NOT_FOUND)

        except Shipment.DoesNotExist:
            return Response({"message": "Shipment not found"}, status=status.HTTP_404_NOT_FOUND)
        

        if shipment.status != "Pending":
            return Response({"message": "Shipment is not pending"}, status=status.HTTP_400_BAD_REQUEST)
        

        if driver.role != "driver":
            return Response({"message": "User is not a driver"}, status=status.HTTP_400_BAD_REQUEST)
        

        
        
        shipment.driver = request.user
        shipment.status = "IN_TRANSIT"
        shipment.save()

        return Response(
            {
                "message": "Driver assigned successfully",
                "tracking_id": shipment.tracking_id,
                "driver": f"{shipment.driver.first_name} {shipment.driver.last_name}"
            }, 
            status=200
        )





class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        try:
            token = request.data["refresh"]
            token_obj = RefreshToken(token)
            token_obj.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)