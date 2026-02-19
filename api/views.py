from django.core.serializers import serialize
from rest_framework import viewsets

# from django.shortcuts import render
# from django.http import JsonResponse
from students.models import Student
from .serializer import StudentSerializer, EmployeeSerializer
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from employees.models import Employee
from django.http import Http404
from rest_framework import mixins, generics


# Create your views here.
@api_view(['GET','POST'])
def studentsView(request):
    if request.method == 'GET':
        # Get all tne data from the student table
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True) # many = True because student is multiple
        return Response(serializer.data,status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def studentDetailView(request,pk):
    try:
        student = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StudentSerializer(student)
        return Response(serializer.data,status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# class Employe(APIView):
#     def get(self,request):
#         employees = Employee.objects.all()
#         serializer = EmployeeSerializer(employees, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def post(self,request):
#         serializer = EmployeeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#
# class EmployeeDetail(APIView):
#     def get_object(self,pk):
#         try:
#             return Employee.objects.get(pk=pk)
#         except Employee.DoesNotExist:
#              raise Http404()
#
#     def get(self, request, pk):
#         employee = self.get_object(pk)
#         serializer = EmployeeSerializer(employee)
#         return Response(serializer.data,status=status.HTTP_200_OK)
#
#     def put(self, request, pk):
#         employee = self.get_object(pk)
#         serializer = EmployeeSerializer(employee, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_200_OK)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         employee = self.get_object(pk)
#         employee.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#


#  Mixins
# class Employees(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
#     queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer
#
#     def get(self,request):
#         return self.list(request)
#
#     def post(self,request):
#         return self.create(request)
#
#
# class EmployeeDetail(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
#     queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer
#
#     def get(self,request,pk):
#         return self.retrieve(request,pk)
#
#     def put(self,request,pk):
#         return self.update(request,pk)
#
#     def delete(self,request, pk):
#         return self.destroy(request,pk)
#

#Generics
class Employees(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class EmployeeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'pk'
