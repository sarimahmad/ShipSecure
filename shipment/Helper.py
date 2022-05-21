from .models import *
from accounts.models import *


def DriverAssign_Process(data):
    length = {}
    for i in data:
        ship = WholeShipment.objects.filter(driver=i)
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


def CheckingCompanyHasDriver(company):
    data = Driver.objects.filter(company=company)
    if len(data) == 0:
        return False
    return True


def AllDriversFreeCompany(id):
    company = BasicUser.objects.get(id=id)
    drivers = []
    data = BasicUser.objects.filter(role="Driver")
    for i in data:
        if i.driver.company_id == company.id and i.driver.driver_isBusy == False:
            drivers.append(i)
    return drivers
