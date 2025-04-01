from django.shortcuts import render, get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import CustomUser, Patient, Specialist, Role, Specialization, Disorder, Report
from .serializers import (
    CustomUSerSerializer, PatientSerializer, SpecialistSerializer,
    RoleSerializer, SpecializationSerializer, DisorderSerializer, ReportSerializer
)
from rest_framework_simplejwt.tokens import RefreshToken

# List and Create Roles
@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def list_create_role_view(request):
    if request.method == 'GET':
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Get single role, patch and destroy 
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def retreive_update_destroy_role_view(request, pk):
    role = get_object_or_404(Role, pk=pk)
    if request.method == 'GET':
        serializer = RoleSerializer(role)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PATCH':
        serializer = RoleSerializer(role, data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)        
    elif request.method == 'DELETE':
        role_name = role.name
        role.delete()
        return Response({'message': f'{role_name} deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    return Response({'error': 'Invalid method'}, status=status.HTTP_401_UNAUTHORIZED)

# List and Create Custom Users
@api_view(['GET', 'POST'])
@permission_classes([permissions.AllowAny])
def list_create_user_view(request):
    if request.method == 'GET':
        users = CustomUser.objects.all()
        serializer = CustomUSerSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = CustomUSerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve, Update, and Delete a User
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def retreive_update_destroy_user_view(request, pk):
    try:
        user = CustomUser.objects.get(pk=pk)
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CustomUSerSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PATCH':
        serializer = CustomUSerSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        user_name = user.username
        user.delete()
        return Response({'message': f'{user_name} deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    
# User login with token
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def user_login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email and not password:
        return Response({'error': 'Both Email and Password are required!'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        return Response({'error': "User does not exist"}, status=status.HTTP_204_NO_CONTENT)
    
    user.check_password(user.password, password)

    refresh_token = RefreshToken.for_user(user)
    access_token = str(refresh_token.access_token)

    return Response({
        "user_id": user.id,
        "user_email": user.email,
        "access_token": access_token,
        "refresh_token": str(refresh_token),
        "message": "Login Successful",
    }, status=status.HTTP_200_OK)

# List and Create Patients
@api_view(['GET', 'POST'])
def list_create_patient_view(request):
    if request.method == 'GET':
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Get single patient, patch and destroy 
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def retreive_update_destroy_patient_view(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'GET':
        serializer = RoleSerializer(patient)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PATCH':
        serializer = RoleSerializer(patient, data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)        
    elif request.method == 'DELETE':
        patient_name = patient.user.username
        patient.delete()
        return Response({'message': f'{patient_name} deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    return Response({'error': 'Invalid method'}, status=status.HTTP_401_UNAUTHORIZED)

# create list specialization
@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def list_create_specialization_view(request):
    if request.method == 'GET':
        specializations = Specialization.objects.all()
        serializer = SpecializationSerializer(specializations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = SpecializationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Specialization created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# retreive, update destroy specialization
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def retreive_update_delete_specialization_view(request, pk):
    specialization = get_object_or_404(Specialization, pk = pk)
    if request.method == 'GET':
        serializer = SpecializationSerializer(specialization)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PATCH':
        serializer = SpecializationSerializer(specialization, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        specialization_name = specialization.name
        specialization.delete()
        return Response({'message': f'{specialization_name} deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# List and Create Specialists
@api_view(['GET', 'POST'])
def list_create_specialist_view(request):
    if request.method == 'GET':
        specialists = Specialist.objects.all()
        serializer = SpecialistSerializer(specialists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = SpecialistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Get single specialist, patch and destroy 
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def retreive_update_destroy_specialist_view(request, pk):
    specialist = get_object_or_404(Specialist, pk=pk)
    if request.method == 'GET':
        serializer = SpecialistSerializer(specialist)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PATCH':
        serializer = SpecialistSerializer(specialist, data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)        
    elif request.method == 'DELETE':
        specialist_name = specialist.user.username
        specialist.delete()
        return Response({'message': f'{specialist_name} deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    return Response({'error': 'Invalid method'}, status=status.HTTP_401_UNAUTHORIZED)

# List and Create Disorders
@api_view(['GET', 'POST'])
def list_create_disorder_view(request):
    if request.method == 'GET':
        disorders = Disorder.objects.all()
        serializer = DisorderSerializer(disorders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = DisorderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Get single disorder, patch and destroy 
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def retreive_update_destroy_disorder_view(request, pk):
    disorder = get_object_or_404(Disorder, pk=pk)
    if request.method == 'GET':
        serializer = DisorderSerializer(disorder)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PATCH':
        serializer = DisorderSerializer(disorder, data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)        
    elif request.method == 'DELETE':
        disorder_name = disorder.name
        disorder.delete()
        return Response({'message': f'{disorder_name} deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    return Response({'error': 'Invalid method'}, status=status.HTTP_401_UNAUTHORIZED)

# List and Create Reports
@api_view(['GET', 'POST'])
def list_create_report_view(request):
    if request.method == 'GET':
        reports = Report.objects.all()
        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = ReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Get single report, patch and destroy 
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def retreive_update_destroy_report_view(request, pk):
    report = get_object_or_404(Report, pk=pk)
    if request.method == 'GET':
        serializer = ReportSerializer(report)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PATCH':
        serializer = ReportSerializer(report, data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)        
    elif request.method == 'DELETE':
        patient_name = report.patient
        report.delete()
        return Response({'message': f'Report for {patient_name} deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    return Response({'error': 'Invalid method'}, status=status.HTTP_401_UNAUTHORIZED)
