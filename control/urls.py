from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'homepage'),
    path('rng/', views.rng, name = 'rng'),
    path('qft/', views.qft, name = 'qft'),
    path('shor/', views.shor, name = 'shor'),
    path('grover/', views.grover, name = 'grover')
]