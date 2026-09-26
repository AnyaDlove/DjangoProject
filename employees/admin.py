from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Employee, EmployeeImage, EmployeeSkill, Skill


class EmployeeImageInline(admin.TabularInline):
    model = EmployeeImage
    extra = 1


@admin.register(Employee)
class EmployeeAdmin(UserAdmin):
    inlines = [EmployeeImageInline]

    fieldsets = UserAdmin.fieldsets + (
        (
            "Дополнительно",
            {
                "fields": (
                    "gender",
                    "middle_name",
                    "description",
                    "hire_date",
                    "role",
                )
            },
        ),
    )


admin.site.register(Skill)
admin.site.register(EmployeeSkill)
