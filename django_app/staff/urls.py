from django.urls import path
from staff import views

urlpatterns = [
    path('', views.DepartmentsTreeView.as_view(), name='department_tree'),
]
