
from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from .models import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['full_name', 'email', 'department', 'job_title']


class EmployeeAccountForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.all().order_by('username'),
        required=False,
        empty_label='No account linked',
        label='Login account',
    )

    class Meta:
        model = Employee
        fields = ['user']


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                'An account with this email address already exists.'
            )

        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            employee_group, created = Group.objects.get_or_create(
                name='Employee'
            )
            user.groups.add(employee_group)

        return user