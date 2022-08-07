from rest_framework import serializers
from .models import Devices


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Devices # this is the model that is being serialized
        fields = '__all__'
        read_only_fields = ['id']
