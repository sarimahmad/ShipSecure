from django.db import models
from phonenumber_field.modelfields import PhoneNumber
from accounts.models import BasicUser
from django.utils import timezone
from django.db.models.signals import post_delete
from django.dispatch import receiver


# Create your models here.
class SenderReceiver(models.Model):
    lat = models.DecimalField(('Latitude'), max_digits=20, decimal_places=16, blank=True, null=True)
    lng = models.DecimalField(('Latitude'), max_digits=20, decimal_places=16)
    address = models.CharField(max_length=300, blank=True, null=True)
    city = models.CharField(max_length=300, blank=True, null=True)
    building = models.CharField(max_length=30)
    name = models.CharField(max_length=300, blank=True, null=True)
    phone = models.CharField(max_length=13, blank=True, null=True)
    streetNo = models.CharField(max_length=100)
    flootUnit = models.CharField(max_length=50)


class Vehicles(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True)
    weight = models.PositiveBigIntegerField()
    image = models.ImageField(upload_to="Vehicle_Images/")
    unique_id = models.CharField(max_length=30, unique=True, default="1")

    def __str__(self):
        return self.name


class WholeShipment(models.Model):
    payment_choices = (
        ("Cash", "Cash"),
        ("Credit/Debit", "Credit/Debit")
    )
    productName = models.CharField(max_length=100, null=True, blank=True)
    productType = models.CharField(max_length=100, null=True, blank=True)
    productQuantity = models.PositiveIntegerField(null=True, blank=True)
    productDescription = models.CharField(max_length=600, null=True, blank=True)
    paymentMethod = models.CharField(max_length=20, choices=payment_choices, default="Cash")
    user = models.ForeignKey(BasicUser, on_delete=models.CASCADE, related_name="Customer_all_Shipment")
    sender = models.ForeignKey(SenderReceiver, related_name="sender_whole_shipment", on_delete=models.CASCADE)
    receiver = models.ForeignKey(SenderReceiver, related_name="receiver_whole_shipment", on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicles, on_delete=models.CASCADE)
    distance = models.DecimalField(('distance'), max_digits=20, decimal_places=16, blank=True, null=True)
    weight = models.IntegerField(null=True, blank=True)
    Date = models.DateField(default=None, null=True, blank=True)
    driver = models.ForeignKey(BasicUser, on_delete=models.CASCADE, related_name="Assign_to_Driver", null=True,
                               blank=True)

    totalCost = models.IntegerField(null=True, blank=True, default=0)
    company = models.ForeignKey(BasicUser, on_delete=models.CASCADE, related_name="Assign_to", null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    Updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.productName


class Status(models.Model):
    shipment = models.ForeignKey(WholeShipment, on_delete=models.CASCADE, related_name="shipment_all_status",
                                 default=None, null=True,
                                 blank=True)
    status = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    Updated_at = models.DateTimeField(default=timezone.now)


# Work when we make query of delete shipment by delete method
@receiver(post_delete, sender=WholeShipment)
def delete_driver_post_delete(sender, instance, *args, **kwargs):
    instance.receiver.delete()
    instance.sender.delete()
