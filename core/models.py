from django.db import models

# Create your models here.

class HealthProgram(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

        
class Client(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    enrolled_programs = models.ManyToManyField(HealthProgram, blank=True)

    def __str__(self):
        return self.name
