from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .models import Employee, Attendance, Credentials, JobRole, Shift, Workcode
from .forms import EmployeeForm, AttendanceForm, JobRoleForm, ShiftForm, WorkcodeForm, ImportScheduleForm, ExportScheduleForm

from .scripts import import_schedule, export_attendance


# Create your views here.
def index_view(request):
	return render(request, 'gestaoassiduidade/index.html')

#Funcionários
def funcionarios_main_view(request):
	context = {'funcs': Employee.objects.select_related('credentials').all(), }
	return render(request, 'gestaoassiduidade/funcionarios/main.html', context)


def funcionarios_new_view(request):
	form = EmployeeForm(request.POST or None, request.FILES)
	if form.is_valid():
		form.save()
		return redirect('gestaoassiduidade:funcionarios_main')
		
	context = {'form': form}
	
	return render(request, 'gestaoassiduidade/funcionarios/new.html', context)

def funcionarios_edit_view(request, func_id):
	func = Employee.objects.get(id_employee=func_id)
	form = EmployeeForm(request.POST or None, instance=func)

	if form.is_valid():
		form.save()
		return HttpResponseRedirect(reverse('gestaoassiduidade:funcionarios_main'))
	
	context = {'form': form, 'func_id': func_id}
	return render(request, 'gestaoassiduidade/funcionarios/edit.html', context)

def funcionarios_remove_view(request, func_id):
	Employee.objects.get(id_employee=func_id).delete()
	return HttpResponseRedirect(reverse('gestaoassiduidade:funcionarios_main'))
	

#Picangens
def picagens_main_view(request):
	context = {'fingers': Attendance.objects.all(), }
	return render(request, 'gestaoassiduidade/picagens/main.html', context)

def picagens_new_view(request):
	form = AttendanceForm(request.POST or None, request.FILES)
	if form.is_valid():
		form.save()
		return redirect('gestaoassiduidade:picagens_main')
		
	context = {'form': form}
	
	return render(request, 'gestaoassiduidade/picagens/new.html', context)


def picagens_edit_view(request, finger_id):
	finger = Attendance.objects.get(id_attendance=finger_id)
	form = AttendanceForm(request.POST or None, instance=finger)

	if form.is_valid():
		form.save()
		return HttpResponseRedirect(reverse('gestaoassiduidade:picagens_main'))
	
	context = {'form': form, 'finger_id': finger_id}
	return render(request, 'gestaoassiduidade/picagens/edit.html', context)


def picagens_remove_view(request, finger_id):
	Attendance.objects.get(id_attendance=finger_id).delete()
	return HttpResponseRedirect(reverse('gestaoassiduidade:picagens_main'))


#Cargos
def cargos_main_view(request):
	context = {'roles': JobRole.objects.all(), }
	return render(request, 'gestaoassiduidade/cargos/main.html', context)

def cargos_new_view(request):
	form = JobRoleForm(request.POST or None, request.FILES)
	if form.is_valid():
		form.save()
		return redirect('gestaoassiduidade:cargos_main')
		
	context = {'form': form}
	
	return render(request, 'gestaoassiduidade/cargos/new.html', context)


def cargos_edit_view(request, role_id):
	role = JobRole.objects.get(id_role=role_id)
	form = JobRoleForm(request.POST or None, instance=role)

	if form.is_valid():
		form.save()
		return HttpResponseRedirect(reverse('gestaoassiduidade:cargos_main'))
	
	context = {'form': form, 'role_id': role_id}
	return render(request, 'gestaoassiduidade/cargos/edit.html', context)


def cargos_remove_view(request, role_id):
	JobRole.objects.get(id_role=role_id).delete()
	return HttpResponseRedirect(reverse('gestaoassiduidade:cargos_main'))


#Turnos
def turnos_main_view(request):
	context = {'shifts': Shift.objects.all(), }
	return render(request, 'gestaoassiduidade/turnos/main.html', context)

def turnos_new_view(request):
	form = ShiftForm(request.POST or None, request.FILES)
	if form.is_valid():
		form.save()
		return redirect('gestaoassiduidade:turnos_main')
		
	context = {'form': form}
	
	return render(request, 'gestaoassiduidade/turnos/new.html', context)


def turnos_edit_view(request, shift_id):
	shift = Shift.objects.get(id_shift=shift_id)
	form = ShiftForm(request.POST or None, instance=shift)

	if form.is_valid():
		form.save()
		return HttpResponseRedirect(reverse('gestaoassiduidade:turnos_main'))
	
	context = {'form': form, 'shift_id': shift_id}
	return render(request, 'gestaoassiduidade/turnos/edit.html', context)


def turnos_remove_view(request, shift_id):
	Shift.objects.get(id_shift=shift_id).delete()
	return HttpResponseRedirect(reverse('gestaoassiduidade:turnos_main'))


#Códigos de trabalho
def codstrabalho_main_view(request):
	context = {'workcodes': Workcode.objects.all(), }
	return render(request, 'gestaoassiduidade/codstrabalho/main.html', context)

def codstrabalho_new_view(request):
	form = WorkcodeForm(request.POST or None, request.FILES)
	if form.is_valid():
		form.save()
		return redirect('gestaoassiduidade:codstrabalho_main')
		
	context = {'form': form}
	return render(request, 'gestaoassiduidade/codstrabalho/new.html', context)


def codstrabalho_edit_view(request, workcode_id):
	code = Workcode.objects.get(id_workcode=workcode_id)
	form = WorkcodeForm(request.POST or None, instance=code)

	if form.is_valid():
		form.save()
		return HttpResponseRedirect(reverse('gestaoassiduidade:codstrabalho_main'))
	
	context = {'form': form, 'workcode_id': workcode_id}
	return render(request, 'gestaoassiduidade/codstrabalho/edit.html', context)


def codstrabalho_remove_view(request, workcode_id):
	Workcode.objects.get(id_workcode=workcode_id).delete()
	return HttpResponseRedirect(reverse('gestaoassiduidade:codstrabalho_main'))


#Import/Export
def import_schedule_view(request):
	form = ImportScheduleForm(request.POST or None, request.FILES)
	if form.is_valid():
		import_schedule.import_schedule(request.FILES["file"], request.POST["work_area"])
		return redirect('gestaoassiduidade:index')
		
	context = {'form': form}
	return render(request, 'gestaoassiduidade/import/schedule.html', context)

def export_attendance_view(request):
	form = ExportScheduleForm(request.POST or None, request.FILES)
	if form.is_valid():
		spreadsheet = export_attendance.export_attendance(form.data['date_begin'], form.data['date_end'])
		response = HttpResponse(spreadsheet, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
		response['Content-Disposition'] = "attachment; filename = registo_assiduidade.xlsx"
		return response
		#return redirect('gestaoassiduidade:index')
		
	context = {'form': form}
	return render(request, 'gestaoassiduidade/export/attendance.html', context)