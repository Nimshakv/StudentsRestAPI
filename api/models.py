from django.db import models
from django.core.validators import validate_email


class Student(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField()
    email = models.EmailField(unique=True, validators=[validate_email])
    class_no = models.CharField(max_length=2)
    parent_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=13, blank=True)
    year = models.CharField(max_length=4, default='2021')

    class Meta:
        ordering = ['-created']
        db_table = 'students'
