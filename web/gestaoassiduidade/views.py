from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Funcionario
from .forms import FuncionarioForm

# Create your views here.
def index_view(request):
	return render(request, 'gestaoassiduidade/index.html')

#Funcionários
def funcionarios_main_view(request):
	context = {'funcs': Funcionario.objects.all()}
	return render(request, 'gestaoassiduidade/funcionarios/main.html', context)


def funcionarios_new_view(request):
	form = FuncionarioForm(request.POST or None, request.FILES)
	if form.is_valid():
		form.save()
		return redirect('gestaoassiduidade:funcionarios_main')
		
	context = {'form': form}
	
	return render(request, 'gestaoassiduidade/funcionarios/new.html', context)

def funcionarios_edit_view(request, func_id):
	func = Funcionario.objects.get(id=func_id)
	form = FuncionarioForm(request.POST or None, instance=func)

	if form.is_valid():
		form.save()
		return HttpResponseRedirect(reverse('gestaoassiduidade:funcionarios_main'))
	
	context = {'form': form, 'func_id': func_id}
	return render(request, 'gestaoassiduidade/funcionarios/edit.html', context)

def funcionarios_remove_view(request, func_id):
	Funcionario.objects.get(id=func_id).delete()
	return HttpResponseRedirect(reverse('gestaoassiduidade:funcionarios_main'))
	

#Picangens
def picagens_view(request):
	return render(request, 'gestaoassiduidade/picagens.html')