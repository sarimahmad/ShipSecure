from django.shortcuts import render
# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from accounts.models import *
from accounts.serializers import CompanyUserSerializer
from rest_framework import status
from .Helper import CheckingCompanyDriverFree, \
    CheckingCompanyHasDriver, \
    DriverAssign_Process, AllDriversFreeCompany


class Addshipment(APIView):
    serializers_class = AddShipmentSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request, format=None):
        data = {"sender": {}, "receiver": {}}
        # print(request.data)
        for key, val in request.data.items():
            if key.startswith("sender"):
                data["sender"][key.split('_', 1)[1]] = val
            elif key.startswith("receiver"):
                data["receiver"][key.split('_', 1)[1]] = val
            else:
                data[key] = val
        # print(data)
        serializers = self.serializers_class(data=data)
        if serializers.is_valid():
            serializers.save(user=request.user)
            serializers_data = serializers.data
            return Response({"Shipment": serializers_data})
        return Response(serializers.errors)


class DeleteShipment(APIView):
    permission_classes = [IsAuthenticated, ]

    def delete(self, request, ship_id, format=None):
        try:
            shipment = WholeShipment.objects.get(pk=ship_id)
        except Exception as e:
            return Response("Shipment Does Not Exits", status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        shipment.delete()
        return Response("Shipment Delete SuccessFully", status=status.HTTP_200_OK)


class GetAllShipment(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, format=None):
        if request.user.role == 'Customer':
            data = request.user.Customer_all_Shipment.all()
            shipments = {"InProgress": [], "Uncompleted": [], "Not_Started": [], "Completed": [], "Cancelled": []}
            for i in data:
                status = StatusSerializer(i.shipment_all_status, many=True).data
                if i.company is None:
                    serializer = GetShipmentSerializer(i)
                    shipments['Uncompleted'].append(serializer.data)

                elif len(status) == 0:
                    serializer = GetShipmentSerializer(i)
                    shipments["Not_Started"].append(serializer.data)
                else:
                    j = status[-1]
                    if j["status"] in [1, 2, 3, 4, 5]:
                        serializer = GetShipmentSerializer(i)
                        serialized_data = serializer.data
                        shipments["InProgress"].append(serialized_data)
                    elif j["status"] == 6:
                        serializer = GetShipmentSerializer(i)
                        serialized_data = serializer.data
                        shipments["Completed"].append(serialized_data)
                    else:
                        serializer = GetShipmentSerializer(i)
                        serialized_data = serializer.data
                        shipments["Cancelled"].append(serialized_data)
            return Response(shipments)
        elif request.user.role == 'Company':
            data = request.user.Assign_to.all()
            shipments = {"InProgress": [], "Uncompleted": [], "Not_Started": [], "Completed": [], "Cancelled": []}
            for i in data:
                status = StatusSerializer(i.shipment_all_status, many=True).data
                if len(status) == 0:
                    serializer = GetShipmentSerializer(i)
                    serialized_data = serializer.data
                    shipments["Not_Started"].append(serialized_data)
                else:
                    j = status[-1]
                    if j["status"] in [1, 2, 3, 4, 5]:
                        serializer = GetShipmentSerializer(i)
                        serialized_data = serializer.data
                        shipments["InProgress"].append(serialized_data)
                    elif j["status"] == 6:
                        serializer = GetShipmentSerializer(i)
                        serialized_data = serializer.data
                        shipments["Completed"].append(serialized_data)
                    else:
                        serializer = GetShipmentSerializer(i)
                        serialized_data = serializer.data
                        shipments["Cancelled"].append(serialized_data)
            return Response(shipments)
        else:
            data = request.user.Assign_to_Driver.all()
            shipments = {"InProgress": [], "Uncompleted": [], "Not_Started": [], "Completed": [], "Cancelled": []}
            for i in data:
                status = StatusSerializer(i.shipment_all_status, many=True).data
                if len(status) == 0:
                    serializer = GetShipmentSerializer(i)
                    serialized_data = serializer.data
                    shipments["Not_Started"].append(serialized_data)
                else:
                    j = status[-1]
                    if j["status"] in [1, 2, 3, 4, 5]:
                        serializer = GetShipmentSerializer(i)
                        serialized_data = serializer.data
                        shipments["InProgress"].append(serialized_data)
                    elif j["status"] == 6:
                        serializer = GetShipmentSerializer(i)
                        serialized_data = serializer.data
                        shipments["Completed"].append(serialized_data)
                    else:
                        serializer = GetShipmentSerializer(i)
                        serialized_data = serializer.data
                        shipments["Cancelled"].append(serialized_data)
            return Response(shipments)
        return Response("Some thing Wrong Happened", status=status.HTTP_404_NOT_FOUND)


class AssignShipment(APIView):
    # permission_classes = [IsAuthenticated, ]

    def post(self, request, format=None):
        C_id = request.data['c_id']
        S_id = request.data['s_id']
        try:
            shipment = WholeShipment.objects.get(pk=S_id)
        except Exception as e:
            return Response("Shipment Does Not Exits", status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        result = CheckingCompanyDriverFree(C_id)
        if result:
            shipment.company_id = C_id
            shipment.save()
            return Response("Shipment Assign", status=status.HTTP_200_OK)
        else:
            return Response("Driver Not Free", status=status.HTTP_404_NOT_FOUND)


class ShowCompanies(APIView):
    # permission_classes = [IsAuthenticated, ]
    def get(self, request, id, format=None):
        shipment = WholeShipment.objects.get(pk=id)
        city = shipment.sender.city
        vehicle_id = shipment.vehicle.unique_id
        companies = []
        data = BasicUser.objects.filter(role="Company")  # Check of Verification
        for i in data:
            if CheckingCompanyHasDriver(i):
                rates = {}
                if city in i.company.coverage or i.company.allPakistan:
                    company_vehicles_rate = VehicelRate.objects.filter(user_id=i.id)
                    if len(company_vehicles_rate.filter(vehicles__unique_id=vehicle_id)) != 0:
                        company_rate = company_vehicles_rate.get(vehicles__unique_id=vehicle_id).rate
                        data = company_rate * 100 / 19
                        val = CompanyUserSerializer(i)
                        rates["company"] = val.data
                        rates["rate"] = data
                        companies.append(rates)

        return Response(companies, status=status.HTTP_200_OK)


class AssignShipment_toDriver(APIView):
    # permission_classes = [IsAuthenticated, ]

    def post(self, request, id, format=None):
        S_id = id
        # Shipment is assign to that driver that has pass all the checks and has least amount of shipments and
        # if drivers has same amount of shipment then random driver will be selected
        try:
            shipment = WholeShipment.objects.get(id=S_id)
            if shipment.company_id is None:
                return Response("Shipment Has No Company", status=status.HTTP_200_OK)
            if shipment.driver_id is not None:
                return Response("Shipment Has Already Assign", status=status.HTTP_200_OK)
        except Exception as e:
            return Response("Shipment Does Not Exits", status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        try:
            drivers = AllDriversFreeCompany(shipment.company_id)
            value = DriverAssign_Process(drivers)
            shipment.driver = value[0]
            driver = Driver.objects.get(id=value[0].driver.id)
            driver.driver_isBusy = True
            driver.save()
            shipment.save()

        except Exception as e:
            return Response("Company Has no Driver", status=status.HTTP_404_NOT_FOUND)

        return Response("Shipment Assign to Driver SuccessFully", status=status.HTTP_200_OK)


# Time and Date of Change Status is reamining You Have to add and Object
# You Have Make Table of Status and Every Shipment has 6 statues that a driver can add or change

class ShowVehiclesCategory(APIView):
    # permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        serializer = VehicleSerializer(Vehicles.objects.all(), many=True)
        serialized_data = serializer.data
        return Response(serialized_data, status=status.HTTP_200_OK)


class Change_Status(APIView):
    # permission_classes = [IsAuthenticated, ]
    serializers_class = StatusSerializer

    def post(self, request, format=None):
        serializers = self.serializers_class(data=request.data)
        if serializers.is_valid():
            serializers.save()
            serializers_data = serializers.data
            return Response({"Status_Updated": serializers_data})
        return Response(serializers.errors)


class GetShipmentDetails(APIView):
    def get(self, request, id):
        shipment = WholeShipment.objects.get(id=id)
        serializers = GetShipmentSerializer(shipment)
        serializers_data = serializers.data
        return Response(serializers_data, status=status.HTTP_200_OK)


class AssignCostToShipment(APIView):
    def post(self, request):
        rate = int(request.data['rate'])
        S_id = request.data['s_id']
        print(rate)
        try:
            shipment = WholeShipment.objects.get(pk=S_id)
        except Exception as e:
            return Response("Shipment Does Not Exits", status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        shipment.totalCost = rate
        shipment.save()
        return Response("Shipment rate Assign")
