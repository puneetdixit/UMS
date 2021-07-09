from django.db import models

# Create your models here.

class StudentModel(models.Model):
    reg_no = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30, null=False)
    last_name = models.CharField(max_length=30)
    father_name = models.CharField(max_length=30, null=False)
    mother_name = models.CharField(max_length=30, null=False)
    # dob = dob = models.DateField(max_length=8, null=False)
    contact_number = models.CharField(max_length=30, null=False, unique=True)
    email = models.EmailField(max_length = 254, null=False, unique=True)
    address = models.CharField(max_length=50, null=False)
    city = models.CharField(max_length=30, null=False)
    state = models.CharField(max_length=30, null=False)
    country = models.CharField(max_length=30, null=False)
    
class Courses(models.Model):
    course_id = models.IntegerField(primary_key=True)
    course_name = models.CharField(max_length=100, null=False, unique=True)
    total_semester = models.IntegerField(null=False)

class Streams(models.Model):
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE)
    stream_id = models.IntegerField(primary_key=True)
    stream_name = models.CharField(max_length=50, null=False)

class Subjects(models.Model):
    stream_id = models.ForeignKey(Streams, on_delete=models.CASCADE)
    subject_name = models.CharField(max_length=50, null=False, unique=True)
    semester = models.IntegerField(null=False)



def update_auto_increment(start, table_name):
    """Update our increments"""
    from django.db import connection, transaction
    cursor = connection.cursor()
    q = "ALTER table {} AUTO_INCREMENT={}".format(table_name, start)
    c = cursor.execute(q)
    print("Update auto increment", c)
    transaction.commit()

# update_auto_increment(20210001, "ums_studentmodel")