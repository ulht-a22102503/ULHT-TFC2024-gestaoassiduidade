from django.db import models


# Create your models here.
class Picagem(models.Model):
    ID_funcionario = models.IntegerField()
    ID_biometria = models.IntegerField() #is this needed? Maybe only if multiple fingers are enrolled
    timestamp = models.DateField()

class Funcionario(models.Model):
    ID_funcionario = models.IntegerField()
    ID_biometria = models.IntegerField(blank=True)
    nome = models.CharField(max_length=200)