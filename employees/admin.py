from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Employee, EmployeeSkill, Skill

admin.site.register(Employee, UserAdmin)
admin.site.register(Skill)
admin.site.register(EmployeeSkill)
