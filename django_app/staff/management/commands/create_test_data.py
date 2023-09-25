import random
from time import time

from django.core.management.base import BaseCommand
from faker import Faker

from staff.models import Department, Employee

EMPLOYEES_COUNT = 50_000
EMPLOYEES_CREATION_BATCH_SIZE = 3000

departments_sample = ['General Management', 'Marketing Department', 'Operations Department',
                      'Finance Department', 'Sales Department', 'Human Resource Department',
                      'Purchase Department']


def _create_departments(parent: None | Department,
                        depth: int,
                        departments_list: None | list[Department] = None) -> list[Department]:
    """
    Recursive creation of test departments and writing them to the database.
    Args:
        parent: (None | Department) Field for building a tree structure.
        depth: (int) Recursion depth.
        departments_list: (None | list[Department]) Storage for created Department objects.
    Returns: (list[Department])
        List of created Department objects.
    """
    if departments_list is None:
        departments_list = []

    if depth == 0:
        return departments_list

    for _ in range(2 if parent else 1):
        name = random.choice(departments_sample) + f' №{str(random.randint(0, 999))}'
        department = Department.objects.create(name=name, parent=parent)
        departments_list.append(department)
        _create_departments(department, depth - 1, departments_list)

    return departments_list


def _create_employees(employees_count: int,
                      batch_size: int,
                      departments_list: list[Department],
                      fake_object: Faker) -> None:
    """
    Generates and writes batches of test employees to the database.
    Args:
        employees_count: (int) Number of objects to be created.
        batch_size: (int) Batch size for group writing in database.
        departments_list: (list[Department]) Data for the related field - department.
        fake_object: (Faker) Object from external lib to creating random data for Employee object.
    Returns: (None)
    """
    employees = []

    for _ in range(employees_count):
        employee = Employee(
            first_name=fake_object.first_name(),
            last_name=fake_object.last_name(),
            position=fake_object.job(),
            hire_date=fake_object.date_between(start_date='-1y', end_date='today'),
            salary=random.randint(50_000, 200_000),
            department=random.choice(departments_list),
        )
        employees.append(employee)

        if len(employees) >= batch_size:
            Employee.objects.bulk_create(employees)
            employees.clear()

    if employees:
        Employee.objects.bulk_create(employees)


class Command(BaseCommand):
    help = 'Generate random departments and employees'

    def handle(self, *args, **kwargs):
        fake = Faker()
        time_start = time()
        departments = _create_departments(parent=None, depth=5)
        _create_employees(employees_count=EMPLOYEES_COUNT,
                          batch_size=EMPLOYEES_CREATION_BATCH_SIZE,
                          departments_list=departments,
                          fake_object=fake)
        time_finish = time()
        spent_time = round(time_finish - time_start, 2)
        self.stdout.write(self.style.SUCCESS(
            f'Successfully created {len(departments)} '
            f'departments and {EMPLOYEES_COUNT} employees.\n'
            f'Time spent on creation: {spent_time} sec.'
        ))
