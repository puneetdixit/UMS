from django.shortcuts import render
from django.http import HttpResponse
from ums.models import *
import json

# Create your views here.

def error(err):
    return HttpResponse(json.dumps({"status": "error", "desc": str(err)}, indent=4))

def success(data=None):
    if not data:
        data = True
    return HttpResponse(json.dumps({"status": "success", "data": data}, indent=4))

def get_student_data(request):
    first_name = request.GET.get('first_name')
    father_name = request.GET.get('father_name')
    mother_name = request.GET.get('mother_name')
    contact_number = request.GET.get('contact')
    email = request.GET.get('email')
    address = request.GET.get('address')
    city = request.GET.get('city')
    state = request.GET.get('state')
    country = request.GET.get('country')
    try:
        StudentModel(first_name=first_name, father_name=father_name, mother_name=mother_name,
                    contact_number=contact_number,email=email,address=address,city=city,state=state, country=country).save()
        return success()
    except Exception as e:
        return error(e)

def add_course(request):
    course_id = request.GET.get('course_id')
    course_name = request.GET.get('course_name')
    total_semester = request.GET.get('total_semester')
    try:
        Courses(course_id, course_name, total_semester).save()
        return success()
    except Exception as e:
        return error(e)

def add_stream(request):
    course_id = request.GET.get('course_id')
    stream_id = request.GET.get('stream_id')
    stream_name = request.GET.get('stream_name')
    try:
        Streams(course_id_id=course_id, stream_id=stream_id, stream_name=stream_name).save()
        return success("Stream added sucessfully.")
    except Exception as e:
        return error(e)

def add_subject(request):
    subject_name = request.GET.get('subject_name')
    semester = request.GET.get('semester')
    stream_id = request.GET.get('stream_id')
    try:
        Subjects(stream_id_id=stream_id, subject_name=subject_name, semester=semester).save()
        return success()
    except Exception as e:
        return error(e)

def get_all_course(request):
    """Join on multiple tables using filter"""
    temp = {}
    data = Subjects.objects.filter(stream_id__course_id = 123)
    for i in data:
        temp[i.stream_id.course_id.course_name] = 1
    return success(temp)
