from rest_framework import serializers
from shipment.models import Vehicles
from .models import *
from django.contrib.auth.models import Group


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicles
        fields = '__all__'


class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicUser
        fields = ('password',)

    def run_validation(self, data):
        user = self.context['request'].user
        print(data.get('old_password'))
        if not user.check_password(data.get('old_password')):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance


class BasicUserSerializer(serializers.ModelSerializer):
    group = serializers.IntegerField(write_only=True)
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = BasicUser
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        group = validated_data.pop('group')
        user = super().create(validated_data)
        data = Group.objects.get(pk=group)
        user.groups.add(data)
        user.set_password(password)
        user.save()
        return user


# Forgot Password Are Remaining

class commpanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = (
            'name', 'owner_Name', 'mailing_address', 'coverage', 'allPakistan', 'website', 'cnic', 'profile',
            'Ntn_number',
            'Ntn_picture', 'Registration_Certificate')


class CompanyUserSerializer(serializers.ModelSerializer):
    company = commpanySerializer(required=True)
    group = serializers.IntegerField(write_only=True)
    groups = GroupSerializer(many=True, read_only=True)
    vehicle = VehicleSerializer(many=True, read_only=True)

    class Meta:
        model = BasicUser
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        company_data = validated_data.pop('company')
        group_data = validated_data.pop('group')
        group = Group.objects.get(pk=group_data)
        # vehicle = company_data.pop('vehicle')
        company = Company.objects.create(**company_data)
        # for i in Vehicles.objects.all():
        #     company.vehicle.add(i)
        user = BasicUser.objects.create(**validated_data, company=company)
        user.groups.add(group)
        user.set_password(password)
        user.save()
        return user


class GetCompany(serializers.ModelSerializer):
    company = commpanySerializer(required=True)
    group = serializers.IntegerField(write_only=True)
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = BasicUser
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}


# Many = True in Many to Many relation


# Driver Part


# For more than one field Always Use many in Serializers and every where and this is
# very important you always forgot in dongeraaa
# You Waste Half Hour on this

class DriverSerializer(serializers.ModelSerializer):
    company = CompanyUserSerializer(read_only=True)
    vehicle_driver = VehicleSerializer(read_only=True, many=True)

    class Meta:
        model = Driver
        fields = (
            'profile', 'cnic_front', 'cnic_back', 'vehicle_driver', 'driver_onWork', 'driver_isBusy', 'company')


class GetAllDriverSerializer(serializers.ModelSerializer):
    company = CompanyUserSerializer(read_only=True)
    driver = DriverSerializer(required=True)
    group = serializers.IntegerField(write_only=True)
    groups = GroupSerializer(many=True, read_only=True)
    vehicle = VehicleSerializer(many=True, read_only=True)

    class Meta:
        model = BasicUser
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}


class CreateDriverSerializer(serializers.ModelSerializer):
    company = CompanyUserSerializer(read_only=True)
    vehicle_driver = serializers.SlugRelatedField(slug_field='unique_id', queryset=Vehicles.objects.all(), many=True)

    class Meta:
        model = Driver
        fields = (
            'profile', 'cnic_front', 'cnic_back', 'vehicle_driver', 'driver_onWork', 'driver_isBusy', 'company')


class DriverUserSerializer(serializers.ModelSerializer):
    company = CompanyUserSerializer(read_only=True)
    driver = CreateDriverSerializer(required=True)
    group = serializers.IntegerField(write_only=True)
    groups = GroupSerializer(many=True, read_only=True)
    vehicle = VehicleSerializer(many=True, read_only=True)

    class Meta:
        model = BasicUser
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        company = validated_data.pop('company')
        driver_data = validated_data.pop('driver')
        group_data = validated_data.pop('group')
        group = Group.objects.get(pk=group_data)
        vehicle_drivers = driver_data.pop('vehicle_driver')
        driver = Driver.objects.create(**driver_data, company=company)
        for vehicle in vehicle_drivers:
            driver.vehicle_driver.add(vehicle)
        user = BasicUser.objects.create(**validated_data, driver=driver)
        user.groups.add(group)
        user.set_password(password)
        user.save()
        return user


class AddCompanyVehicle_Serializer(serializers.ModelSerializer):
    company = CompanyUserSerializer(read_only=True)
    type = serializers.SlugRelatedField(slug_field='unique_id', queryset=Vehicles.objects.all())

    class Meta:
        model = Company_Vehicles
        fields = '__all__'


class ShowCompanyVehicles(serializers.ModelSerializer):
    type = VehicleSerializer(read_only=True)

    class Meta:
        model = Company_Vehicles
        fields = '__all__'


class VehicleRateSerializer(serializers.ModelSerializer):
    vehicles = serializers.SlugRelatedField(slug_field='unique_id', queryset=Vehicles.objects.all())

    class Meta:
        model = VehicelRate
        fields = ('rate', 'vehicles', 'user')


class GetVehicleRateSerializer(serializers.ModelSerializer):
    vehicles = VehicleSerializer(read_only=True)

    class Meta:
        model = VehicelRate
        fields = ('vehicles', 'rate')


class ChangeVehicleRateSerializer(serializers.ModelSerializer):
    vehicles = serializers.SlugRelatedField(slug_field='unique_id', queryset=Vehicles.objects.all())

    class Meta:
        model = VehicelRate
        fields = ('vehicles', 'rate', 'user')

    def validate(self, attrs):
        if attrs.get('rate') > 100000:
            raise serializers.ValidationError({"Bad": "Rate is Too High"})
        else:
            print("Good")
        return attrs

    def update(self, instance, validated_data):
        instance.rate = validated_data.get('rate', instance.rate)
        instance.save()
        return instance


class Update_Customer_ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicUser
        fields = ('first_name', 'last_name', 'city', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.city = validated_data.get('city', instance.city)
        instance.profile = validated_data.get('profile', instance.profile)
        instance.save()
        return instance

# class DriverTimeTableSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DriverTimeTable
#         fields = ('driver', 'time')


# class LoginSerializers(serializers.Serializer):
#     email = serializers.CharField(max_length=255)
#     password = serializers.CharField(
#         style={'input_type': 'password'},
#         trim_whitespace=False,
#         max_length=128,
#         write_only=True
#     )
#     def validate(self, data):
#         username = data.get('email')
#         password = data.get('password')

#         if username and password:
#             user = authenticate(request=self.context.get('request'),
#                                 username=username, password=password)
#             if not user:
#                 msg = ('Unable to log in with provided credentials.')
#                 raise serializers.ValidationError(msg, code='authorization')
#         else:
#             msg = ('Must include "username" and "password".')
#             raise serializers.ValidationError(msg, code='authorization')

#         data['user'] = user
#         return data


# class CompanySerializer(serializers.ModelSerializer):
# email = serializers.EmailField(source='user.email', read_only=True)
# group = serializers.IntegerField(write_only = True)
# groups = GroupSerializer(many=True, read_only=True)

# class Meta:
#     model = CompanyData
#     fields = '__all__'
#     extra_kwargs = {
#         'password': {'write_only': True, 'min_length': 4},
#         'groups': {'read_only': True,},
#         'user':{'read_only': True,}
#     }
# def create(self, validated_data):
#     group = validated_data.pop('group')
#     user = super().create(**validated_data)
#     data = Group.objects.get(pk=group)
#     user.groups.add(data)
#     return user
