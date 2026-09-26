from django.core.exceptions import ValidationError
from django.db import models

from employees.models import Employee


class Workplace(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    desk_number = models.CharField(max_length=10)
    extra_info = models.TextField(blank=True, null=True)

    def clean(self):
        super().clean()
        if not self.desk_number or not self.employee:
            return
        if not self.employee.role:
            return
        try:
            desk = int(self.desk_number)
        except (TypeError, ValueError):
            return
        if self.employee.role != "tester":
            return
        for neighbor in [desk - 1, desk + 1]:
            for nw in Workplace.objects.filter(desk_number=str(neighbor)).exclude(
                pk=self.pk
            ):
                if nw.employee.role in ["frontend", "backend"]:
                    raise ValidationError(
                        f"Стол {desk} нельзя ставить рядом со столом {neighbor}: "
                        f"тестировщик и разработчик не могут сидеть за соседними столами."
                    )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Стол {self.desk_number} ({self.employee})"
