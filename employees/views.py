from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import Employee


def home(request):
    total_employees = Employee.objects.count()
    latest_employees = Employee.objects.prefetch_related("images").order_by(
        "-hire_date"
    )[:4]
    return render(
        request,
        "employees/home.html",
        {
            "total_employees": total_employees,
            "latest_employees": latest_employees,
        },
    )


def employee_list(request):
    employees_qs = Employee.objects.prefetch_related("images").order_by("-hire_date")
    paginator = Paginator(employees_qs, 10)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "employees/employee_list.html", {"page_obj": page_obj})


@login_required
def employee_detail(request, pk):
    employee = get_object_or_404(
        Employee.objects.prefetch_related("images", "employeeskill_set__skill"), pk=pk
    )
    return render(request, "employees/employee_detail.html", {"employee": employee})
