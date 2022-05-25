# Create your views he
import json
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import BasicUser
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import update_last_login


# Create your views here.
class LoginApi(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data['email']
        password = request.data['password']
        user = BasicUser.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User Not Found')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect Password')

        if user.role == "Customer":
            data = BasicUserSerializer(user)
        elif user.role == "Company":
            if not user.is_Verified:
                return Response("Your Company is Not Verified", status=status.HTTP_404_NOT_FOUND)
            data = CompanyUserSerializer(user)
        else:
            data = GetAllDriverSerializer(user)
        # user_logged_in.send(sender=user.__class__, request=request, user=user) if we do this it send signal every time
        # from django.contrib.auth.models import update_last_login check using this
        update_last_login(None, user)
        refresh = RefreshToken.for_user(user)
        responce_data = {
            'access_token': str(refresh.access_token),
            'user': data.data
        }
        return Response(responce_data, status=status.HTTP_200_OK)


class RegisterApi(APIView):
    serializers_class = BasicUserSerializer

    def post(self, request):
        serializers = self.serializers_class(data=request.data)
        if serializers.is_valid():
            user = serializers.save()
            refresh = RefreshToken.for_user(user)
            data = serializers.data
            responce_data = {
                'access_token': str(refresh.access_token),
                'user': data
            }

            return Response(responce_data, status=status.HTTP_200_OK)
        else:
            return Response(serializers.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, id):
        object = BasicUser.objects.get(id=id)
        print(request.data)
        serializers = ChangePasswordSerializer(instance=object, data=request.data, context={'request': request})
        if serializers.is_valid():
            serializers.save()
            responce_data = {
                "Sucess": "Your Password has Been Changed"
            }

            return Response(responce_data, status=status.HTTP_200_OK)
        else:
            return Response(serializers.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class VerifyOtp(APIView):

    def post(self, request):
        data = request.data
        user_obj = BasicUser.objects.get(email=data['phone'])
        if int(user_obj.otp) == int(data['otp']):
            user_obj.is_Verified = True
            user_obj.save()
            return Response({"Status": 200, "message": "Your Number has Been Verified You can Login Now"},
                            status=status.HTTP_200_OK)
        else:
            return Response({"Status": 404, "message": "Your OTP is Wrong"},
                            status=status.HTTP_404_NOT_FOUND)
        return Response({"Status": 422, "message": "No User with This Number Detects"},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class Verify_User(APIView):

    def post(self, request, id):
        user_obj = BasicUser.objects.get(id=id)
        user_obj.is_Verified = True
        user_obj.save()
        return Response("User Verified", status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class CompanyApi(APIView):
    serializers_class = CompanyUserSerializer

    # permission_classes = [IsAuthenticated,]
    def post(self, request):

        data = {'company': {}}
        for key, val in request.data.items():
            if key == 'name' or key == 'owner_Name' or key == 'cnic' or key == 'website' or key == 'Ntn_number' or key == 'Ntn_number' or key == 'cnic_front' or key == 'cnic_back' or key == 'Ntn_picture' or key == 'Registration_Certificate':
                data['company'][key] = val
            else:
                data[key] = val

        serializers = self.serializers_class(data=data)
        if serializers.is_valid():
            user = serializers.save()
            user.save()
            refresh = RefreshToken.for_user(user)
            data = serializers.data
            responce_data = {
                'access_token': str(refresh.access_token),
                'user': data
            }
            return Response(responce_data, status=status.HTTP_200_OK)
        else:
            return Response(serializers.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class AddDriverApi(APIView):
    serializers_class = DriverUserSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        data = {"driver": {}}
        print(request.data)
        for key, val in request.data.items():
            if key == 'profile' or key == 'cnic_front' or key == 'cnic_back' or key == 'License':
                data["driver"][key] = val
            elif key == 'vehicle_driver':
                data["driver"][key] = json.loads(val)
            else:
                if key == 'number':
                   data[key]=int(val)
                else:
                    data[key] = val
        serializers = self.serializers_class(data=data)
        if serializers.is_valid():

            user = serializers.save(company=request.user)
            user.save()
            refresh = RefreshToken.for_user(user)
            data1 = serializers.data

            responce_data = {
                'access_token': str(refresh.access_token),
                'user': data1
            }
            return Response(responce_data, status=status.HTTP_200_OK)
        else:
            return Response(serializers.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def get(self, request):
        data = request.user.Company_Driver.all()

        drivers = []
        data = BasicUser.objects.filter(role="Driver")
        for i in data:
            if i.driver.company_id == request.user.id:
                drivers.append(i)
        serializer = GetAllDriverSerializer(drivers, many=True)
        serialized_data = serializer.data
        return Response(serialized_data)


class DeleteDriver(APIView):
    permission_classes = [IsAuthenticated, ]

    def delete(self, request, key_id):
        try:
            driver = BasicUser.objects.get(id=key_id, role="Driver")
        except Exception as e:
            return Response("User Does Not Exits", status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        driver.delete()
        return Response("Your Driver Has Been Deleted", status=status.HTTP_200_OK)


# You are right, even after you remove the JWT token it remains valid token for a period of time until it expires.
# JWT is stateless. So if you want to handle logout and to invalidate token you must need to keep a database or
# in memory cache to store the invalid(blacklisted) token.


# class LogOut_User(APIView):
#     permission_classes = [IsAuthenticated, ]
#
#     def get(self, request, *args, **kwargs):
#         print(request.auth)
#         return Response("User SuccessFully Logout", status=status.HTTP_200_OK)


class AddCompanyVehicle(APIView):
    serializers_class = AddCompanyVehicle_Serializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        data = request.data
        serializers = self.serializers_class(data=data)
        if serializers.is_valid():
            user = serializers.save(company=request.user)
            user.save()
            data = serializers.data

            responce_data = {
                'Sucess': "Vehcile Added",
                'user': data
            }
            return Response(responce_data, status=status.HTTP_200_OK)
        else:
            return Response(serializers.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def get(self, request):
        data = request.user.All_Vehicles.all()
        serializer = ShowCompanyVehicles(data, many=True)
        serialized_data = serializer.data
        return Response(serialized_data)


class VehiclesRate(APIView):
    serializers_class = VehicleRateSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        data = request.data
        serializers = self.serializers_class(data=data)
        if serializers.is_valid():
            user = serializers.save(user=request.user)
            user.save()
            data = serializers.data
            responce_data = {
                'Sucess': "Done",
                'user': data
            }
            return Response(responce_data, status=status.HTTP_200_OK)
        else:
            return Response(serializers.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def get(self, request):
        print(request.user)
        data = request.user.Vehicles_rate.all()
        serializer = GetVehicleRateSerializer(data, many=True)
        serialized_data = serializer.data
        return Response(serialized_data)

    def put(self, request):

        obj = VehicelRate.objects.filter(user=request.user)
        for i in obj:
            if i.vehicles.unique_id == request.data['vehicles']:
                serializers = ChangeVehicleRateSerializer(instance=i, data=request.data)
                if serializers.is_valid():
                    serializers.save()
                    serialized_data = serializers.data
                    return Response({"New Rate": serialized_data})
                else:
                    return Response(serializers.errors)


# Can be Done in Another way by Checking the time on the Shipment that assign to driver if the date
# is same that use is selecting than we can warn

# Check Here that Driver is By using Company Id and checking that any driver of
# vehicle type that has been selected has shipment of this
# this date which is incomplete
# if shipment is is completed that means driver is free
# return Response({"Status": "Driver is Free", "Code": 1}, status=status.HTTP_200_OK)


class GetDriverDetails(APIView):
    # permission_classes = [IsAuthenticated, ]

    def get(self, request, id):
        driver = BasicUser.objects.get(id=id)
        serializers = GetAllDriverSerializer(driver)
        serializers_data = serializers.data
        return Response(serializers_data, status=status.HTTP_200_OK)


class ShowCompanyVehicleDetails(APIView):
    # permission_classes = [IsAuthenticated, ]

    def get(self, request, id):
        vehicle = Company_Vehicles.objects.get(id=id)
        serializers = ShowCompanyVehicles(vehicle)
        serializers_data = serializers.data
        return Response(serializers_data, status=status.HTTP_200_OK)
