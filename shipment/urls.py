from django.urls import path
from .views import *

urlpatterns = [
    path('', Addshipment.as_view(), name='Add_Shipment'),
    path('deleteShipment/<int:ship_id>', DeleteShipment.as_view(), name="Delete_Shipment"),
    path('assginShipment/', AssignShipment.as_view(), name="AssignShipment"),
    path('Assign_shipment_Driver/<int:id>/', AssignShipment_toDriver.as_view(), name='Assign_shipment_Driver_api'),
    path('Get_All_Shipment/', GetAllShipment.as_view(), name="GetShipmentAll"),
    path('ShowCompanies/<int:id>/', ShowCompanies.as_view() ,name='SHow_Companies'),
    path('Al_Vehicle_Cat/', ShowVehiclesCategory.as_view(), name='Al_Vehicle_Cat'),
    path('update_status/', Change_Status.as_view(), name='Change_Status'),
    path('Check_DriverTime/', Checking_Driver_free.as_view(), name='Driver_Time_api'),
    path('ShipmentDetails/<int:id>/', GetShipmentDetails.as_view(), name='Shipment_Details_api'),
    path('ShipmentCost/', AssignCostToShipment.as_view(), name='Shipment_Details_api'),
]
