from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Client, HealthProgram, Enrollment
from .serializers import ClientSerializer, HealthProgramSerializer, EnrollmentSerializer

class HealthProgramViewSet(viewsets.ModelViewSet):
    queryset = HealthProgram.objects.all()
    serializer_class = HealthProgramSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    @action(detail=True, methods=['post'])
    def enroll(self, request, pk=None):
        """Enroll client in one or more programs"""
        client = self.get_object()
        program_ids = request.data.get('program_ids', [])

        if not isinstance(program_ids, list):
            return Response({"error": "program_ids should be a list of IDs"}, status=400)

        enrollments = []
        for pid in program_ids:
            program = HealthProgram.objects.get(id=pid)
            enrollment, _ = Enrollment.objects.get_or_create(client=client, program=program)
            enrollments.append(enrollment)

        return Response(EnrollmentSerializer(enrollments, many=True).data, status=201)
