from django.db import models

# Create your models here.

class StudentModel(models.Model):
    reg_no = models.IntegerField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    father_name = models.CharField(max_length=30)
    mother_name = models.CharField(max_length=30)
    dob = dob = models.DateField(max_length=8)
    contact_number = models.CharField(max_length=30)
    email = models.EmailField(max_length = 254)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    