from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Employee
from .serializers import (EmployeeDetailSerializer, EmployeeListSerializer,
                          EmployeeWriteSerializer)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.prefetch_related(
        "images", "employeeskill_set__skill"
    ).order_by("-hire_date")
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return EmployeeListSerializer
        if self.action == "retrieve":
            return EmployeeDetailSerializer
        return EmployeeWriteSerializer
