from django.urls import path
from gestaoassiduidade import views

urlpatterns = [
    path('', views.index_view, name='index'),
]
