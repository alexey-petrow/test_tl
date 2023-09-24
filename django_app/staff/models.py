from django.db import models

from config.abstract_models import UUIDMixin, TimeStampedMixin


class Department(UUIDMixin):
    name = models.CharField(verbose_name='department name', max_length=255)
    parent = models.ForeignKey(to='self', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'departments'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'parent'],
                name='unique_combination_of_name_and_parent'
            ),
        ]

    def __str__(self):
        return self.name


class Employee(UUIDMixin, TimeStampedMixin):
    first_name = models.CharField(verbose_name='first name', max_length=255)
    last_name = models.CharField(verbose_name='last name', max_length=255)
    middle_name = models.CharField(verbose_name='middle name', max_length=255, blank=True)
    position = models.CharField(verbose_name='position', max_length=255)
    hire_date = models.DateField(verbose_name='hire date')
    salary = models.DecimalField(verbose_name='salary in rubles', max_digits=10, decimal_places=2)
    department = models.ForeignKey(to=Department, null=True,
                                   on_delete=models.SET_NULL, related_name='employees')

    @property
    def full_name(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'

    class Meta:
        ordering = ['-hire_date']
        verbose_name_plural = 'employees'

    def __str__(self):
        return self.full_name
