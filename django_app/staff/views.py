from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import ListView

from staff.models import Department


@method_decorator(cache_page(2), name='dispatch')
class DepartmentsTreeView(ListView):
    template_name = 'department_tree.html'
    context_object_name = 'departments'
    extra_context = {'title': 'Departments tree'}
    queryset = (Department.objects
                .prefetch_related('subdepartments', 'employees')
                .filter(parent__isnull=True))
