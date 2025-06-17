from django import forms
from django.forms import ModelForm
from .models import Employee, Attendance, JobRole, Shift

class EmployeeForm(ModelForm):
    class Meta:
            model = Employee
            fields = ['name','id_role']

class AttendanceForm(ModelForm):
    class Meta:
            model = Attendance
            fields = '__all__'

class JobRoleForm(ModelForm):
    class Meta:
            model = JobRole
            fields = '__all__'

class ShiftForm(ModelForm):
    class Meta:
            model = Shift
            fields = '__all__'
