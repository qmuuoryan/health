from rest_framework import serializers
from .models import Client, HealthProgram, Enrollment

class HealthProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthProgram
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    program = HealthProgramSerializer(read_only=True)
    program_id = serializers.PrimaryKeyRelatedField(
        queryset=HealthProgram.objects.all(), source='program', write_only=True
    )

    class Meta:
        model = Enrollment
        fields = ['id', 'program', 'program_id', 'enrolled_on']

class ClientSerializer(serializers.ModelSerializer):
    enrollments = EnrollmentSerializer(source='enrollment_set', many=True, read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'name', 'age', 'gender', 'contact_info', 'enrollments']
