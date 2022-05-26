from django.db import models
from django.db.models.base import Model
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
import random



class Company(models.Model):
    name = models.CharField(max_length=255, blank=True)
    owner_Name = models.CharField(max_length=255, blank=True)
    coverage = models.JSONField(null=True, blank=True)
    mailing_address = models.CharField(max_length=1000, blank=True)
    allPakistan = models.BooleanField(default=False)
    website = models.CharField(max_length=200, null=True, blank=True)
    cnic = models.CharField(max_length=13)
    profile = models.ImageField(upload_to="Company_profile/", null=True, blank=True)
    Ntn_number = models.CharField(max_length=15)
    Ntn_picture = models.ImageField(upload_to="Ntn_Number/", null=True, blank=True)
    Registration_Certificate = models.ImageField(upload_to="Registration_Certificate/", null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class Driver(models.Model):
    profile = models.ImageField(upload_to="Driver_profile/", null=True, blank=True)
    cnic_front = models.ImageField(upload_to="Driver/Cnic_front/", null=True, blank=True)
    company = models.ForeignKey("accounts.BasicUser", related_name="Company_Driver", on_delete=models.CASCADE,
                                default=None, blank=True, null=True)
    cnic_back = models.ImageField(upload_to="Driver/Cnic_back/", null=True, blank=True)
    License = models.ImageField(upload_to="Driver/License/", null=True, blank=True)
    cnic_back = models.ImageField(upload_to="Driver/Cnic_back/", null=True, blank=True)

    vehicle_driver = models.ManyToManyField(to="shipment.Vehicles")
    driver_onWork = models.BooleanField(default=True)
    driver_isBusy = models.BooleanField(default=False)


class BasicUser(AbstractUser):
    Regitser_choice = (
        ('Customer', 'Customer'),
        ('Company', 'Company'),
        ('Driver', 'Driver'),
    )
    username = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(verbose_name='email', max_length=255, unique=True, blank=True, null=True, error_messages={
        'null': 'This feild cannot be nulll'
    })
    password = models.CharField(max_length=255, blank=True, null=True)
    number = models.CharField(max_length=13,blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=10, choices=Regitser_choice)
    is_Verified = models.BooleanField(default=False)
    profile = models.ImageField(upload_to="Customer_profile/", null=True, blank=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    company = models.OneToOneField(Company, on_delete=models.CASCADE, default=None, blank=True, null=True)
    driver = models.OneToOneField(Driver, on_delete=models.CASCADE, default=None, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    Updated_at = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.email} {self.role}"


# class DriverTimeTable(models.Model):
#     driver = models.ForeignKey(BasicUser,on_delete=models.CASCADE)
#     time = models.DateTimeField(unique=True, default=None)

class Company_Vehicles(models.Model):
    name = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    type = models.ForeignKey("shipment.Vehicles", on_delete=models.CASCADE, default=None)
    registration_number = models.CharField(max_length=255)
    registration_city = models.CharField(max_length=255)
    Vehicle_Busy = models.BooleanField(default=False)
    company = models.ForeignKey(BasicUser, related_name="All_Vehicles", on_delete=models.CASCADE, default=None)


class VehicelRate(models.Model):
    user = models.ForeignKey(BasicUser, related_name="Vehicles_rate", on_delete=models.CASCADE, default=None)
    vehicles = models.ForeignKey("shipment.Vehicles", on_delete=models.CASCADE, default=None)
    rate = models.IntegerField()


# Work on Signal It is very HelpFull and Interesting
@receiver(post_delete, sender=BasicUser)
def delete_driver_post_delete(sender, instance, *args, **kwargs):
    if instance.role =='Company':
        instance.company.delete()
    else:
         instance.driver.delete()



@receiver(post_save, sender=BasicUser)
def send_email_post_save(sender, instance, created, *args, **kwargs):
    if instance.role == 'Driver' or instance.role == 'Customer':
        pass
    else:
        if created:
            try:
                otp_to_send = random.randint(1000, 9999)
                instance.otp = otp_to_send
                instance.save()
                subject = "Your Email Needs to be Verified"
                message = f"Hi , Thanks for Registering Your Company" \
                          f"We Have received Your Credentials" \
                          f"We will Sent you a mail after approving your Company" \
                          f"It will take Some Time Thanks "
                email_from = settings.EMAIL_HOST_USER
                email_to = [instance.email]
                send_mail(subject, message, email_from, email_to)
            except Exception as e:
                print("error")
                print(e)



# Send Mail to company when its verified use If created

@receiver(post_save, sender=BasicUser)
def Verified_post_save(sender,created, instance, *args, **kwargs):
    if instance.is_active == False:
        if instance.is_Verified:
            try:
                print("signal")
                instance.is_active = True
                instance.save()
                subject = "Your Email is Verified"
                message = f"Hi , Your Can Login Now" \
                          f"Congratulations"
                email_from = settings.EMAIL_HOST_USER
                email_to = [instance.email]
                send_mail(subject, message, email_from, email_to)
            except Exception as e:
                print(e)
