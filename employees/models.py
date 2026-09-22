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
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, blank=True, null=True
    )
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username


class EmployeeSkill(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    level = models.IntegerField(choices=[(i, i) for i in range(1, 11)])

    def __str__(self):
        return f"{self.employee} - {self.skill} ({self.level})"
