from django.db import models

class HealthProgram(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Client(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]

    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField(default=0)
    gender = models.CharField(default= 0, max_length=1, choices=GENDER_CHOICES)
    contact_info = models.TextField(default=0)

    programs = models.ManyToManyField('HealthProgram', through='Enrollment')

    def __str__(self):
        return self.name

class Enrollment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    program = models.ForeignKey(HealthProgram, on_delete=models.CASCADE)
    enrolled_on = models.DateField(auto_now_add=True)
