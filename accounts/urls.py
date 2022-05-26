from .views import *
from django.urls import path

urlpatterns = [
    path('', LoginApi.as_view(), name='login_view'),
    path('signUp/', RegisterApi.as_view(), name='Customer_register_api'),
    path('CompanySignUp/', CompanyApi.as_view(), name='Company_register_api'),
    path('DriverSignUp/', AddDriverApi.as_view(), name='Driver_register_api'),
    path('GetAllDriver/', AddDriverApi.as_view(), name='Get_all_Driver_api'),
    path('AddCompanyVehicle/', AddCompanyVehicle.as_view(), name='Add_CompanyVehicle_api'),
    path('GetCompanyVehicle/', AddCompanyVehicle.as_view(), name='Add_CompanyVehicle_api'),
    path('VehicleRate/', VehiclesRate.as_view(), name='Vehicle_Rate_api'),
    path('DeleteDriver/<int:key_id>/', DeleteDriver.as_view(), name='DeleteDriver_api'),
    path('DeleteVehicle/<int:key_id>/', DeleteVehicle.as_view(), name='DeleteVehicle_api'),
    path('VerifyOtp/', VerifyOtp.as_view(), name='Verify_Otp_api'), # Not Using
    path('ChangePassword/<int:id>/', ChangePassword.as_view(), name='Change_Password_api'),
    path('Verify_User/<int:id>/', Verify_User.as_view(), name='Verify_User_api'),
    path('GetDriverDetails/<int:id>/', GetDriverDetails.as_view(), name='GetDriver_Details_api'),
    path('GetCompanyDetails/<int:id>/', ShowCompanyVehicleDetails.as_view(), name='Show_Company_Vehicle_Details_api'),
    path('UpdateCustomer_Profile/<int:id>/', UpdateProfile.as_view(), name='Update_Customer_Profile_api'),
]
