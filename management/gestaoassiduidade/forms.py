from django import forms
from django.forms import ModelForm
from .models import Employee, Attendance

class EmployeeForm(ModelForm):
    class Meta:
            model = Employee
            fields = ['name',]

class AttendanceForm(ModelForm):
    class Meta:
            model = Attendance
            fields = '__all__'
