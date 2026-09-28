from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from employees.models import Employee, EmployeeSkill, Skill
from workplaces.models import Workplace


class URLsTests(TestCase):
    def setUp(self):
        self.employee = Employee.objects.create_user(
            username="testuser",
            password="testpass123",
            first_name="Иван",
            last_name="Иванов",
            gender="M",
            hire_date=date.today() - timedelta(days=100),
            role="backend",
        )

    def test_home_page_available(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_employee_list_available(self):
        response = self.client.get(reverse("employee_list"))
        self.assertEqual(response.status_code, 200)

    def test_employee_detail_redirects_anonymous(self):
        response = self.client.get(reverse("employee_detail", args=[self.employee.pk]))
        self.assertEqual(response.status_code, 302)

    def test_employee_detail_available_when_logged_in(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("employee_detail", args=[self.employee.pk]))
        self.assertEqual(response.status_code, 200)


class ContextTests(TestCase):
    def setUp(self):
        self.employee = Employee.objects.create_user(
            username="ctxuser",
            password="testpass123",
            first_name="Пётр",
            last_name="Петров",
            gender="M",
            hire_date=date.today() - timedelta(days=10),
            role="backend",
        )
        self.skill = Skill.objects.create(name="Python")
        EmployeeSkill.objects.create(employee=self.employee, skill=self.skill, level=8)

    def test_home_context_has_total_employees(self):
        response = self.client.get(reverse("home"))
        self.assertIn("total_employees", response.context)
        self.assertIn("latest_employees", response.context)
        self.assertEqual(response.context["total_employees"], 1)

    def test_employee_list_uses_pagination(self):
        response = self.client.get(reverse("employee_list"))
        self.assertIn("page_obj", response.context)

    def test_employee_detail_context(self):
        self.client.login(username="ctxuser", password="testpass123")
        response = self.client.get(reverse("employee_detail", args=[self.employee.pk]))
        self.assertEqual(response.context["employee"].pk, self.employee.pk)


class WorkplaceValidatorTests(TestCase):
    def setUp(self):
        self.tester = Employee.objects.create_user(
            username="tester1",
            password="testpass123",
            first_name="Тест",
            last_name="Тестов",
            role="tester",
        )
        self.backend = Employee.objects.create_user(
            username="backend1",
            password="testpass123",
            first_name="Бэк",
            last_name="Бэков",
            role="backend",
        )

    def test_tester_cannot_sit_next_to_backend(self):
        Workplace.objects.create(employee=self.backend, desk_number="3")

        with self.assertRaises(ValidationError):
            Workplace.objects.create(employee=self.tester, desk_number="2")

    def test_tester_can_sit_far_from_backend(self):
        Workplace.objects.create(employee=self.backend, desk_number="3")

        workplace = Workplace.objects.create(employee=self.tester, desk_number="7")
        self.assertEqual(workplace.desk_number, "7")
