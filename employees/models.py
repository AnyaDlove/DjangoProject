from datetime import date

from django.contrib.auth.models import AbstractUser
from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Employee(AbstractUser):
    GENDER_CHOICES = [
        ("M", "Мужской"),
        ("F", "Женский"),
    ]
    ROLE_CHOICES = [
        ("tester", "Тестировщик"),
        ("frontend", "Фронтендер"),
        ("backend", "Бекендер"),
    ]
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, blank=True, null=True
    )
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    hire_date = models.DateField(blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.username

    @property
    def days_in_company(self):
        if not self.hire_date:
            return 0
        return (date.today() - self.hire_date).days


class EmployeeImage(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="employees/")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Фото {self.employee} #{self.order}"


class EmployeeSkill(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    level = models.IntegerField(choices=[(i, i) for i in range(1, 11)])

    def __str__(self):
        return f"{self.employee} - {self.skill} ({self.level})"
