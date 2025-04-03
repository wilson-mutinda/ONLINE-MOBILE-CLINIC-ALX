from rest_framework import serializers
from .models import CustomUser, Patient, Specialist, Role, Specialization, Disorder, Report
import re
from django.core.validators import RegexValidator

# Role Serializer
class RoleSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    class Meta:
        model = Role
        fields = ['id', 'name']

    def validate_name(self, name):
        name = name.lower().strip()
        role_name = ['admin', 'patient', 'specialist']

        if name not in role_name:
            raise serializers.ValidationError(f"Invalid Role. Allowed roles: {', '.join(role_name)}")
        return name

# Customuser serializer
class CustomUSerSerializer(serializers.ModelSerializer):

    email = serializers.EmailField()
    role = RoleSerializer()
    password = serializers.CharField(write_only = True)
    confirm_password = serializers.CharField(write_only = True)

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'role', 'password', 'confirm_password', 'is_admin']

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        # Check if passwords match
        if password and confirm_password and password != confirm_password:
            raise serializers.ValidationError("Password Mismatch!")
        
        # check password length
        if len(password) < 8:
            raise serializers.ValidationError("Password should have more than 8 characters")
        
        # password to contain at least one digit
        if not re.search(r'\d', password):
            raise serializers.ValidationError("Passwords must contain at least one digit")
        
        return data
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')

        # role data
        role_data = validated_data.pop('role')
        role_name = role_data.get('name').lower().strip()

        # fetch role data
        role, _ = Role.objects.get_or_create(name = role_name)
        validated_data['role'] = role

        # Automatically set is_Admin True if role is admin
        if role_name == 'admin':
            validated_data['is_admin'] = True

        # create customuser
        user = CustomUser.objects.create_user(**validated_data)
        return user

# patient serializer
class PatientSerializer(serializers.ModelSerializer):

    user = CustomUSerSerializer()    
    phone = serializers.CharField(validators = [
        RegexValidator(regex=r'^(01|07)\d{8}$', message="Invalid Phone Number!")
    ])
    class Meta:
        model = Patient
        fields = ['id', 'user', 'phone', 'date_of_birth', 'address']

    def validate_phone(self, phone):
        if len(phone) != 10:
            raise serializers.ValidationError("Invalid Phone Number!")
        
        if not (phone.startswith("01") or phone.startswith("07")):
            raise serializers.ValidationError("Invalid Phone Number")
        
        return phone
    
    def create(self, validated_data):

        # fetch user from validated data
        user_data = validated_data.pop('user')
        role_data = user_data.pop('role')
        role_name = role_data.get('name')

        if role_name != 'patient':
            raise serializers.ValidationError("Invalid role.Please use 'patient' instead!")
        
        role, _ = Role.objects.get_or_create(name = role_name)

        # create user
        user = CustomUser.objects.create_user(role=role, **user_data)

        # create patient
        patient = CustomUser.objects.create(user = user, **validated_data)
        return patient
    
# specialization Serializer   
class SpecializationSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    class Meta:
        model = Specialization
        fields = ['id', 'name']

    def validate_name(self, name):
        specialization_name = ['dentist', 'nurse', 'doctor']
        if not name in specialization_name:
            raise serializers.ValidationError("Invalid Specialization Name!")
        return name

# specialist serializer
class SpecialistSerializer(serializers.ModelSerializer):
    user = CustomUSerSerializer()
    specialization = SpecializationSerializer()
    phone = serializers.CharField(validators = [
        RegexValidator(regex=r'^(07|01)\d{8}$', message="Invalid Phone Number!")
    ])
    date_of_birth = serializers.DateField()

    class Meta:
        model = Specialist
        fields = ['id', 'user', 'specialization', 'phone', 'date_of_birth']

    def validate_phone(self, phone):
        if len(phone) != 10:
            raise serializers.ValidationError("Invali Phone number")
        
        if not (phone.startswith("01") or phone.startswith("07")):
            raise serializers.ValidationError("Invalid Phone Number!")
        
        return phone
    
    def create(self, validated_data):

        # fetch user data
        user_data = validated_data.pop('user')
        specialization_data = validated_data.pop('specialization')

        # validate specialization
        specialization_name = specialization_data.get('name')
        specialization_instance, _ = Specialization.objects.get_or_create(name = specialization_name)

        # validate role
        role_data = user_data.pop('role')
        role_name = role_data.get('name').lower()

        if role_name != 'specialist':
            raise serializers.ValidationError("Invalid role.Please use 'specialist' instead!")
        
        role_instance, _ = Role.objects.get_or_create(name='specialist')

        # create custom user
        user = CustomUser.objects.create_user(role = role_instance, **user_data)

        specialist = Specialist.objects.create(user = user, specialization=specialization_instance, **validated_data)
        return specialist

# disorder serializer
class DisorderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disorder
        fields = ['id', 'name', 'description']

# Report serializer
class ReportSerializer(serializers.ModelSerializer):
    patient = PatientSerializer()
    specialist = SpecialistSerializer()
    disorder = DisorderSerializer()
    date_created = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Report
        fields = ['id', 'patient', 'specialist', 'disorder', 'date_created']

    def validate_patient(self, patient):
        if not Patient.objects.filter(id=patient.id).exists():
            raise serializers.ValidationError("Invalid Patient ID")
        return patient

    def create(self, validated_data):

        # retreive nested objects
        patient_data = validated_data.pop('patient')
        specialist_data = validated_data.pop('specialist')
        disorder_data = validated_data.pop('disorder')

        # create or retreive patient
        user_data = patient_data.pop('user')
        role_data = user_data.pop('role')
        role, _ = Role.objects.get_or_create(name='patient')
        user = CustomUser.objects.create_user(role=role, **user_data)
        patient = Patient.objects.create(user=user, **patient_data)

        # create or retreive specialis
        specialist_user_data = specialist_data.pop('user')
        specialization_data = specialist_data.pop('specialization')
        role_specialist, _ = Role.objects.get_or_create(name = 'specialist')
        specialist_user = CustomUser.objects.create_user(role = role_specialist, **specialist_user_data)
        specialization, _ = Specialization.objects.get_or_create(name = specialization_data.get('name'))
        specialist = Specialist.objects.create(user=specialist_user, specialization = specialization, **specialist_data)

        # create or retreive disorder
        disorder, _ = Disorder.objects.get_or_create(**disorder_data)

        # create report
        report = Report.objects.create(patient=patient, specialist=specialist, disorder=disorder, **validated_data)
        return report
    
