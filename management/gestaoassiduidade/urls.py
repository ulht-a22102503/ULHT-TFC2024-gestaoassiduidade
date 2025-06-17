from django.urls import path
from gestaoassiduidade import views

app_name = "gestaoassiduidade"

urlpatterns = [
    path('', views.index_view, name='index'),
    #Funcionarios
    path('funcionarios/', views.funcionarios_main_view, name='funcionarios_main'),
    path('funcionarios/new', views.funcionarios_new_view, name='funcionarios_new'),
    path('funcionarios/edit/<int:func_id>', views.funcionarios_edit_view, name='funcionarios_edit'),
    path('funcionarios/remove/<int:func_id>', views.funcionarios_remove_view, name='funcionarios_remove'),
    #Picagens
    path('picagens/', views.picagens_main_view, name = 'picagens_main'),
    path('picagens/new', views.picagens_new_view, name = 'picagens_new'),
    path('picagens/edit/<int:finger_id>', views.picagens_edit_view, name = 'picagens_edit'),
    path('picagens/remove/<int:finger_id>', views.picagens_remove_view, name = 'picagens_remove'),
    #Cargos
    path('cargos/', views.cargos_main_view, name = 'cargos_main'),
    path('cargos/new', views.cargos_new_view, name = 'cargos_new'),
    path('cargos/edit/<str:role_id>', views.cargos_edit_view, name = 'cargos_edit'),
    path('cargos/remove/<str:role_id>', views.cargos_remove_view, name = 'cargos_remove'),
]
