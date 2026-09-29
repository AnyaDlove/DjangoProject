from rest_framework import serializers

from .models import Employee, EmployeeImage, EmployeeSkill, Skill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "name"]


class EmployeeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeImage
        fields = ["id", "image", "order"]


class EmployeeSkillSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)

    class Meta:
        model = EmployeeSkill
        fields = ["id", "skill", "level"]


class EmployeeListSerializer(serializers.ModelSerializer):
    skills = EmployeeSkillSerializer(
        source="employeeskill_set", many=True, read_only=True
    )
    days_in_company = serializers.IntegerField(read_only=True)

    class Meta:
        model = Employee
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "role",
            "days_in_company",
            "skills",
        ]


class EmployeeDetailSerializer(serializers.ModelSerializer):
    skills = EmployeeSkillSerializer(
        source="employeeskill_set", many=True, read_only=True
    )
    images = EmployeeImageSerializer(many=True, read_only=True)
    days_in_company = serializers.IntegerField(read_only=True)

    class Meta:
        model = Employee
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "middle_name",
            "email",
            "gender",
            "role",
            "description",
            "hire_date",
            "days_in_company",
            "skills",
            "images",
        ]


class EmployeeWriteSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Employee
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "middle_name",
            "email",
            "gender",
            "role",
            "description",
            "hire_date",
            "password",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        employee = Employee(**validated_data)
        if password:
            employee.set_password(password)
        employee.save()
        return employee

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
