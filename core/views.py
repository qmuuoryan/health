from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Client, HealthProgram, Enrollment
from .serializers import ClientSerializer, HealthProgramSerializer, EnrollmentSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count



class HealthProgramViewSet(viewsets.ModelViewSet):
    queryset = HealthProgram.objects.all()
    serializer_class = HealthProgramSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'contact_info']
    filterset_fields = ['gender', 'age']

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


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'age', 'gender', 'contact_info']

class EnrollmentForm(forms.Form):
    programs = forms.ModelMultipleChoiceField(
        queryset=HealthProgram.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

@login_required
def home(request):
    context = {
        'total_clients': Client.objects.count(),
        'total_programs': HealthProgram.objects.count(),
        'total_enrollments': Enrollment.objects.count(),
    }
    return render(request, 'core/home.html', context)

@login_required
def register_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Client registered successfully.")
            return redirect('client_list')
        else:
            messages.error(request, "Failed to register client. Please correct the form.")
    else:
        form = ClientForm()
    return render(request, 'core/register_client.html', {'form': form})

@login_required
def client_list(request):
    query = request.GET.get('q')
    if query:
        clients = Client.objects.filter(name__icontains=query)
    else:
        clients = Client.objects.all()
    return render(request, 'core/client_list.html', {'clients': clients, 'query': query})

@login_required
def enroll_client(request, client_id):
    client = Client.objects.get(id=client_id)
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            for program in form.cleaned_data['programs']:
                Enrollment.objects.get_or_create(client=client, program=program)
            messages.success(request, f"{client.name} successfully enrolled.")
            return redirect('client_list')
        else:
            messages.error(request, "Enrollment failed.")
    else:
        form = EnrollmentForm()
    return render(request, 'core/enroll_client.html', {'form': form, 'client': client})

@login_required
def client_profile(request, client_id):
    client = Client.objects.get(id=client_id)
    enrollments = client.enrollment_set.select_related('program')
    return render(request, 'core/client_profile.html', {'client': client, 'enrollments': enrollments})
