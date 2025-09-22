from django.urls import path
from . import views

urlpatterns = [
    path('produto/<str:codigo>/', views.estoque_list, name='estoque_list'),
]