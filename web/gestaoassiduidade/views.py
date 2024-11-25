from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Employee, Attendance, Fingerprint
from .forms import EmployeeForm

# Create your views here.
def index_view(request):
	return render(request, 'gestaoassiduidade/index.html')

#Funcionários
def funcionarios_main_view(request):
	context = {'funcs': Employee.objects.all(),
	'fingers': Fingerprint.objects.all(), }
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
def picagens_view(request):
	context = {'fingers': Attendance.objects.all(), }
	return render(request, 'gestaoassiduidade/picagens.html', context)
