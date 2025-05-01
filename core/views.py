from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import HealthProgram, Client
from .serializers import HealthProgramSerializer, ClientSerializer, ClientEnrollSerializer
from rest_framework.decorators import action

class HealthProgramViewSet(viewsets.ModelViewSet):
    queryset = HealthProgram.objects.all()
    serializer_class = HealthProgramSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    @action(detail=True, methods=['post'])
    def enroll(self, request, pk=None):
        client = self.get_object()
        serializer = ClientEnrollSerializer(data=request.data)
        if serializer.is_valid():
            programs = serializer.validated_data['enrolled_programs']
            client.enrolled_programs.add(*programs)
            return Response({'status': 'enrolled'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
