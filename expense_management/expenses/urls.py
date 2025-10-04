from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('manager-dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('employee-dashboard/', views.employee_dashboard, name='employee_dashboard'),
]
