from rest_framework import serializers
from .models import CustomUser, Patient, Specialist, Role, Specialization, Disorder, Report

# Role Serializer
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

# Custom User Serializer
class CustomUserSerializer(serializers.ModelSerializer):
    role = RoleSerializer()

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'role', 'date_joined', 'is_active', 'is_staff']

# Patient Serializer
class PatientSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Patient
        fields = '__all__'

# Specialization Serializer
class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = '__all__'

# Specialist Serializer
class SpecialistSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    specialization = SpecializationSerializer()

    class Meta:
        model = Specialist
        fields = '__all__'

# Disorder Serializer
class DisorderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disorder
        fields = '__all__'

# Report Serializer
class ReportSerializer(serializers.ModelSerializer):
    patient = PatientSerializer()
    specialist = SpecialistSerializer()
    disorder = DisorderSerializer()

    class Meta:
        model = Report
        fields = '__all__'
