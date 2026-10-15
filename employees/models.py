
from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employee_profile",
    )
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    department = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name