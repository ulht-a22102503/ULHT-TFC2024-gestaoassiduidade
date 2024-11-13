from django import forms
from django.forms import ModelForm
from .models import Funcionario, Picagem

class FuncionarioForm(ModelForm):
    class Meta:
            model = Funcionario
            fields = '__all__'