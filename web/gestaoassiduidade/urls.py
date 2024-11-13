from django.urls import path
from gestaoassiduidade import views

app_name = "gestaoassiduidade"

urlpatterns = [
    path('', views.index_view, name='index'),
    path('funcionarios/', views.funcionarios_main_view, name='funcionarios_main'),
    path('funcionarios/new', views.funcionarios_new_view, name='funcionarios_new'),
    path('funcionarios/edit/<int:func_id>', views.funcionarios_edit_view, name='funcionarios_edit'),
    path('funcionarios/remove/<int:func_id>', views.funcionarios_remove_view, name='funcionarios_remove'),
    path('picagens', views.picagens_view, name = 'picagens'),
]