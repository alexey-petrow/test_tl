from django.contrib import admin

from staff.models import Department, Employee


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'employees_count']
    list_filter = ['parent']
    list_per_page = 20
    search_fields = ['name']

    @admin.display(description='number of employees')
    def employees_count(self, obj):
        return obj.employees_count

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('parent')


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'position',
                    'hire_date', 'salary', 'department']
    list_filter = [('hire_date', admin.DateFieldListFilter),
                   'department']
    list_per_page = 50
    list_select_related = ['department']
    search_fields = ['first_name', 'last_name', 'middle_name']


admin.site.register(Department, DepartmentAdmin)
admin.site.register(Employee, EmployeeAdmin)
