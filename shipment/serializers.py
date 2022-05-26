from rest_framework import serializers
from .models import *
from accounts.serializers import BasicUserSerializer, CompanyUserSerializer, GetAllDriverSerializer, ShowCompanyVehicles


class SenderReceiverSerializer(serializers.ModelSerializer):
    class Meta:
        model = SenderReceiver
        fields = '__all__'


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicles
        fields = '__all__'


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ('shipment', 'status', 'created_at', 'Updated_at')


class GetShipmentSerializer(serializers.ModelSerializer):
    user = BasicUserSerializer(read_only=True)
    company = CompanyUserSerializer(read_only=True)
    real_vehicle = ShowCompanyVehicles(read_only=True)
    sender = SenderReceiverSerializer()
    receiver = SenderReceiverSerializer()
    driver = GetAllDriverSerializer(read_only=True)
    shipment_all_status = StatusSerializer(many=True)
    vehicle = VehicleSerializer()

    class Meta:
        model = WholeShipment
        fields = '__all__'
        read_only_fields = ('company',)



class AddShipmentSerializer(serializers.ModelSerializer):
    user = BasicUserSerializer(read_only=True)
    sender = SenderReceiverSerializer()
    receiver = SenderReceiverSerializer()
    # status = StatusSerializer(read_only=True)
    vehicle = serializers.SlugRelatedField(slug_field='unique_id', queryset=Vehicles.objects.all())

    class Meta:
        model = WholeShipment
        fields = '__all__'
        read_only_fields = ('user',)

    def create(self, validated_data):
        sender_data = validated_data.pop("sender")
        receiver_data = validated_data.pop("receiver")
        sender = SenderReceiver.objects.create(**sender_data)
        receiver = SenderReceiver.objects.create(**receiver_data)
        return WholeShipment.objects.create(**validated_data, sender=sender, receiver=receiver)
