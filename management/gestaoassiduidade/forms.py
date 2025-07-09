from django import forms
from django.forms import ModelForm
from .models import Employee, Attendance, JobRole, Shift, Workcode
from django.core.validators import FileExtensionValidator
from datetime import date

IMPORT_SCHEDULE_CHOICES = [
    ('ERPI', 'Lar'),
    ('SAD',"Apoio Domiciliário"),
    ('LAV',"Lavandaria"),
    ('COZ', 'Cozinha'),
]


class EmployeeForm(ModelForm):
    class Meta:
            model = Employee
            fields = ['name','id_role']
            labels = {
                'name':'Nome',
                'id_role':'Cargo',
            }
            
class AttendanceForm(ModelForm):
    class Meta:
            model = Attendance
            fields = ['id_employee','timestamp']
            labels = {
                'id_employee':'Nome do trabalhador',
                'timestamp':'Cargo',
            }

class JobRoleForm(ModelForm):
    class Meta:
            model = JobRole
            fields = '__all__'
            labels = {
                'id_role':'Sigla',
                'descript':'Descrição',
            }

class ShiftForm(ModelForm):
    class Meta:
            model = Shift
            fields = ['time_begin','break_begin','break_end','time_end']
            labels = {
                'time_begin':'Início de turno',
                'break_begin':'Início de pausa',
                'break_end':'Fim de pausa',
                'time_end':'Fim de turno',
            }

class WorkcodeForm(ModelForm):
    class Meta:
            model = Workcode
            fields = '__all__'
            labels = {
                'id_workcode':'Código de trabalho',
                'code_type':'É código de presença?',
                'descript':'Descrição',
            }

class ImportScheduleForm(forms.Form):
    file = forms.FileField(label="Ficheiro da escala", validators=[FileExtensionValidator(['csv'])])
    work_area = forms.ChoiceField(label="Resposta Social", choices=IMPORT_SCHEDULE_CHOICES)
    date_begin = forms.DateField(label="Desde dia (DD-MM-AAAA):", input_formats=['%d-%m-%Y'])
    date_end = forms.DateField(label="Até dia (DD-MM-AAAA):", input_formats=['%d-%m-%Y'])

class ExportScheduleForm(forms.Form):
    date_begin = forms.DateField(label="Desde dia (DD-MM-AAAA):", input_formats=['%d-%m-%Y'])
    date_end = forms.DateField(label="Até dia (DD-MM-AAAA):", input_formats=['%d-%m-%Y'])