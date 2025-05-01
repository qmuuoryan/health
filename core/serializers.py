from rest_framework import serializers
from .models import HealthProgram, Client

class HealthProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthProgram
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    enrolled_programs = HealthProgramSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = '__all__'

class ClientEnrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['enrolled_programs']
