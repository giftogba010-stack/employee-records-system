from django.shortcuts import render

# Create your views here.from django.shortcuts import render


def employee_list(request):
    return render(request, "employee_list.html")
