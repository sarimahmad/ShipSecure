from .models import *
from accounts.models import *


def DriverAssign_Process(data):
    length = {}
    for i in data:
        ship = WholeShipment.objects.filter(driver=i)
        length[i] = len(ship)

    value = min(length.items(), key=lambda x: x[1])
    return value

def CheckingCompanyDriver(company):
    data = Driver.objects.filter(company=company)
    for i in data:
        if i.driver_isBusy == False:
            return True
            break
    return False
