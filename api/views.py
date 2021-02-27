from .models import Student
from .serializer import StudentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.core.paginator import Paginator
import json


class StudentList(APIView):
    """
     List all students, or create a new student.
     """

    def get(self, request, format=None):
        try:

            search_params = request.GET.get('search_params', '')
            search_params = json.loads(search_params)
            students = Student.objects.filter(first_name__icontains=search_params['first_name'],
                                              last_name__icontains=search_params['last_name'],
                                              email__icontains=search_params['email'],
                                              parent_name__icontains=search_params['parent'],
                                              phone_number__icontains=search_params['phone_number'],
                                              )

            # exact value filtering
            if search_params['class_no'] != '':
                students = students.filter(class_no__exact=search_params['class_no'])
            if search_params['dob'] != '':
                students = students.filter(dob__exact=search_params['dob'])
            if search_params['year'] != '':
                students = students.filter(year__exact=search_params['year'])
            if search_params['created'] != '':
                date = search_params['created'].split('-')
                students = students.filter(created__year=date[0], created__month=date[1], created__day=date[2])
            if search_params['updated'] != '':
                date = search_params['updated'].split('-')
                students = students.filter(updated__year=date[0], updated__month=date[1], updated__day=date[2])

            # for server side pagination
            total_length = len(students)
            start = int(request.GET.get('start', 0))
            page_count = self.request.query_params.get('length', 25)
            page = int((start / int(page_count)) + 1)
            paginator = Paginator(students, page_count)
            students = paginator.page(page)
            serializer = StudentSerializer(students, many=True)

            return Response(data={
                'result': serializer.data,
                'total_length': total_length
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(data={
                'result': [],
                'total_length': 0
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        try:
            serializer = StudentSerializer(data=request.POST)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(data={}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StudentDetail(APIView):
    """
    Retrieve, update or delete a student instance.
    """

    def get_object(self, pk):
        try:
            return Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        try:
            student = self.get_object(pk)
            student = StudentSerializer(student)
            return Response(student.data)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk, format=None):
        try:
            student = self.get_object(pk)
            serializer = StudentSerializer(student, data=request.POST)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk, format=None):
        try:
            student = self.get_object(pk)
            student.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
