from django.views.generic import ListView
from staff.models import Department


class DepartmentsTreeView(ListView):
    template_name = 'department_tree.html'
    queryset = Department.objects.filter(parent__isnull=True)
    context_object_name = 'departments'
    extra_context = {'title': 'Departments tree'}
