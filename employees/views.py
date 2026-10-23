
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db.models import Q

from .models import Employee
from .forms import (
    EmployeeForm,
    EmployeeAccountForm,
    CustomUserCreationForm,
)


def user_in_group(user, group_name):
    return user.groups.filter(name__iexact=group_name).exists()


def is_admin(user):
    return user.is_superuser or user_in_group(user, 'Admin')


def can_manage_employees(user):
    return is_admin(user) or user_in_group(user, 'HR')


def get_employee_profile(user):
    try:
        return user.employee_profile
    except Employee.DoesNotExist:
        return None


def can_edit_employee(user, employee):
    if can_manage_employees(user):
        return True

    profile = get_employee_profile(user)

    if user_in_group(user, 'Manager'):
        return (
            profile is not None
            and employee.department == profile.department
        )

    if user_in_group(user, 'Employee'):
        return employee.user_id == user.id

    return False


@login_required
def employee_list(request):
    user = request.user
    can_add = can_manage_employees(user)
    profile = get_employee_profile(user)
    search_query = request.GET.get('q', '').strip()

    if can_add:
        employees = Employee.objects.all()
    elif user_in_group(user, 'Manager') and profile:
        employees = Employee.objects.filter(
            department=profile.department
        )
    elif user_in_group(user, 'Employee'):
        employees = Employee.objects.filter(user=user)
    else:
        employees = Employee.objects.none()

    if search_query:
        employees = employees.filter(
            Q(full_name__icontains=search_query)
            | Q(email__icontains=search_query)
            | Q(department__icontains=search_query)
        )

    can_edit = (
        can_add
        or (
            user_in_group(user, 'Manager')
            and profile is not None
        )
        or (
            user_in_group(user, 'Employee')
            and profile is not None
        )
    )

    if request.method == 'POST':
        if not can_add:
            messages.error(
                request,
                'You do not have permission to add employees.'
            )
            return redirect('employee_list')

        form = EmployeeForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Employee added successfully.'
            )
            return redirect('employee_list')
    else:
        form = EmployeeForm()

    return render(request, 'employee_list.html', {
        'employees': employees,
        'form': form,
        'can_add': can_add,
        'can_edit': can_edit,
        'can_delete': can_add,
        'search_query': search_query,
    })


@login_required
def edit_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)

    if not can_edit_employee(request.user, employee):
        messages.error(
            request,
            'You do not have permission to edit this employee.'
        )
        return redirect('employee_list')

    if request.method == 'POST':
        form = EmployeeForm(
            request.POST,
            instance=employee
        )
    else:
        form = EmployeeForm(instance=employee)

    if user_in_group(request.user, 'Manager'):
        form.fields['department'].disabled = True

    if user_in_group(request.user, 'Employee'):
        form.fields['department'].disabled = True
        form.fields['job_title'].disabled = True

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(
            request,
            'Employee updated successfully.'
        )
        return redirect('employee_list')

    return render(request, 'edit_employee.html', {
        'form': form,
        'employee': employee,
    })


@login_required
def link_employee_account(request, employee_id):
    if not can_manage_employees(request.user):
        messages.error(
            request,
            'Only HR or Admin can link employee accounts.'
        )
        return redirect('employee_list')

    employee = get_object_or_404(Employee, id=employee_id)

    if request.method == 'POST':
        form = EmployeeAccountForm(
            request.POST,
            instance=employee
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Employee account linked successfully.'
            )
            return redirect('employee_list')
    else:
        form = EmployeeAccountForm(instance=employee)

    return render(request, 'link_employee_account.html', {
        'form': form,
        'employee': employee,
    })


@login_required
@require_POST
def remove_employee(request, employee_id):
    if not can_manage_employees(request.user):
        messages.error(
            request,
            'You do not have permission to remove employees.'
        )
        return redirect('employee_list')

    employee = get_object_or_404(Employee, id=employee_id)
    employee.delete()

    messages.success(
        request,
        'Employee removed successfully.'
    )
    return redirect('employee_list')


def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(
                request,
                'Registration successful! Welcome.'
            )
            return redirect('employee_list')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {
        'form': form
    })