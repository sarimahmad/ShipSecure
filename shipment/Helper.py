from .models import *
from accounts.models import *


def DriverAssign_Process(data):
    length = {}
    for i in data:
        ship = WholeShipment.objects.filter(driver=i)
        length[i] = len(ship)
    value = min(length.items(), key=lambda x: x[1])
    return value


def VehicleAssign_Process(data):
    length = {}
    for i in data:
        ship = WholeShipment.objects.filter(real_vehicle=i)
        length[i] = len(ship)
    value = min(length.items(), key=lambda x: x[1])
    return value


def CheckingCompanyDriverFree(company):
    data = Driver.objects.filter(company_id=company)
    for i in data:
        if not i.driver_isBusy:
            return True
            break
    return False


def CheckingCompanyVehicleFree(company):
    data = Company_Vehicles.objects.filter(company_id=company)
    for i in data:
        if not i.Vehicle_Busy:
            return True
            break
    return False


def CheckingCompanyHasDriver(company):
    data = Driver.objects.filter(company=company)
    if len(data) == 0:
        return False
    return True


def AllDriversFreeCompany(id):
    drivers = []
    data = BasicUser.objects.filter(role="Driver")
    for i in data:
        if i.driver.company_id == id and i.driver.driver_isBusy == False:
            drivers.append(i)
    return drivers


def AllVehicleFreeCompany(id):
    Vehicles = []
    data = Company_Vehicles.objects.all()
    for i in data:
        if i.company_id == id and i.Vehicle_Busy == False:
            Vehicles.append(i)
    return Vehicles
