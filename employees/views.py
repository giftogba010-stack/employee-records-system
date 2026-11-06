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


# =========================
# ROLE HELPER FUNCTIONS
# =========================

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


# =========================
# PERMISSIONS
# =========================

def can_edit_employee(user, employee):
    """
    Only Admin, HR, and Managers can edit employees.
    Normal Employees cannot edit any employee profile.
    """

    # Admin and HR can edit all employees
    if can_manage_employees(user):
        return True

    # Managers can edit employees in their department
    if user_in_group(user, 'Manager'):
        profile = get_employee_profile(user)

        return (
            profile is not None
            and employee.department == profile.department
        )

    # Normal Employees cannot edit profiles
    return False


# =========================
# EMPLOYEE DASHBOARD / LIST
# =========================

@login_required
def employee_list(request):

    user = request.user

    # Role checks
    can_add = can_manage_employees(user)
    is_employee = user_in_group(user, 'Employee')
    is_manager = user_in_group(user, 'Manager')

    profile = get_employee_profile(user)

    # =========================
    # RESTRICT EMPLOYEE RECORDS
    # =========================

    # Admin and HR can see all employees
    if can_add:
        employees = Employee.objects.all()

    # Managers can see employees in their department
    elif is_manager and profile:
        employees = Employee.objects.filter(
            department=profile.department
        )

    # Normal Employees can ONLY see their own record
    elif is_employee:
        employees = Employee.objects.filter(
            user=user
        )

    # Everyone else sees nothing
    else:
        employees = Employee.objects.none()

    # =========================
    # STATISTICS
    # =========================

    # Statistics are calculated for the accessible records,
    # but will only be displayed to authorized roles in HTML.
    total_employees = employees.count()

    total_departments = (
        employees
        .values('department')
        .distinct()
        .count()
    )

    linked_accounts = employees.filter(
        user__isnull=False
    ).count()

    unlinked_accounts = employees.filter(
        user__isnull=True
    ).count()

    # =========================
    # SEARCH AND FILTER
    # =========================

    search_query = request.GET.get('q', '').strip()
    selected_department = request.GET.get(
        'department', ''
    ).strip()

    # Only Admin/HR/Managers can use search and filters
    can_search = can_add or is_manager

    departments = Employee.objects.none()

    if can_search:

        departments = (
            employees
            .order_by('department')
            .values_list('department', flat=True)
            .distinct()
        )

        # Apply department filter
        if selected_department:
            employees = employees.filter(
                department=selected_department
            )

        # Apply search
        if search_query:
            employees = employees.filter(
                Q(full_name__icontains=search_query)
                | Q(email__icontains=search_query)
                | Q(department__icontains=search_query)
            )

    # =========================
    # EDIT PERMISSIONS
    # =========================

    can_edit = can_add or (
        is_manager and profile is not None
    )

    # =========================
    # ADD EMPLOYEE
    # =========================

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

    # =========================
    # RENDER PAGE
    # =========================

    return render(
        request,
        'employee_list.html',
        {
            'employees': employees,
            'profile': profile,

            # Roles / permissions
            'is_employee': is_employee,
            'is_manager': is_manager,
            'can_add': can_add,
            'can_edit': can_edit,
            'can_delete': can_add,
            'can_search': can_search,

            # Form
            'form': form,

            # Search / filter
            'search_query': search_query,
            'selected_department': selected_department,
            'departments': departments,

            # Statistics
            'total_employees': total_employees,
            'total_departments': total_departments,
            'linked_accounts': linked_accounts,
            'unlinked_accounts': unlinked_accounts,
        }
    )


# =========================
# EDIT EMPLOYEE
# =========================

@login_required
def edit_employee(request, employee_id):

    employee = get_object_or_404(
        Employee,
        id=employee_id
    )

    if not can_edit_employee(
        request.user,
        employee
    ):
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

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Employee updated successfully.'
            )

            return redirect('employee_list')

    else:

        form = EmployeeForm(
            instance=employee
        )

    # Managers cannot change department
    if user_in_group(
        request.user,
        'Manager'
    ):
        form.fields['department'].disabled = True

    return render(
        request,
        'edit_employee.html',
        {
            'form': form,
            'employee': employee,
        }
    )


# =========================
# LINK EMPLOYEE ACCOUNT
# =========================

@login_required
def link_employee_account(request, employee_id):

    # Only Admin or HR can link accounts
    if not can_manage_employees(request.user):

        messages.error(
            request,
            'Only HR or Admin can link employee accounts.'
        )

        return redirect('employee_list')

    employee = get_object_or_404(
        Employee,
        id=employee_id
    )

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

        form = EmployeeAccountForm(
            instance=employee
        )

    return render(
        request,
        'link_employee_account.html',
        {
            'form': form,
            'employee': employee,
        }
    )


# =========================
# REMOVE EMPLOYEE
# =========================

@login_required
@require_POST
def remove_employee(request, employee_id):

    # Only Admin or HR can remove employees
    if not can_manage_employees(request.user):

        messages.error(
            request,
            'You do not have permission to remove employees.'
        )

        return redirect('employee_list')

    employee = get_object_or_404(
        Employee,
        id=employee_id
    )

    employee.delete()

    messages.success(
        request,
        'Employee removed successfully.'
    )

    return redirect('employee_list')


# =========================
# REGISTER USER
# =========================

def register_user(request):

    if request.method == 'POST':

        form = CustomUserCreationForm(
            request.POST
        )

        if form.is_valid():

            user = form.save()

            login(
                request,
                user
            )

            messages.success(
                request,
                'Registration successful! Welcome.'
            )

            return redirect('employee_list')

    else:

        form = CustomUserCreationForm()

    return render(
        request,
        'register.html',
        {
            'form': form
        }
    )


# =========================
# EMPLOYEE DETAILS
# =========================

@login_required
def employee_detail(request, employee_id):

    employee = get_object_or_404(
        Employee,
        id=employee_id
    )

    user = request.user

    # Admin and HR can view every employee
    if can_manage_employees(user):

        return render(
            request,
            'employee_detail.html',
            {
                'employee': employee,
            }
        )

    # Manager can view employees in their department
    if user_in_group(user, 'Manager'):

        profile = get_employee_profile(user)

        if (
            profile is not None
            and employee.department == profile.department
        ):

            return render(
                request,
                'employee_detail.html',
                {
                    'employee': employee,
                }
            )

    # Normal employee can ONLY view their own profile
    if (
        user_in_group(user, 'Employee')
        and employee.user_id == user.id
    ):

        return render(
            request,
            'employee_detail.html',
            {
                'employee': employee,
            }
        )

    messages.error(
        request,
        'You do not have permission to view this employee.'
    )

    return redirect('employee_list')