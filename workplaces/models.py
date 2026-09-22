from django.db import models
from employees.models import Employee


class Workplace(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    desk_number = models.CharField(max_length=10)
    extra_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Стол {self.desk_number} ({self.employee})"