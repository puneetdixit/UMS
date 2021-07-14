from django.shortcuts import render
from django.http import JsonResponse
from ums.models import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.views import obtain_auth_token
import time


from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.contrib.auth.models import auth
from rest_framework.authtoken.models import Token


def error(err):
    return JsonResponse({"status": "error", "desc": str(err)})

def success(data=None):
    if not data:
        data = True
    return JsonResponse({"status": "success", "data": data})

@csrf_exempt 
@api_view(['POST'])
def add_course(request):
    course_name = request.POST.get('course_name')
    duration = request.POST.get('duration')
    try:
        Courses(course_name=course_name, duration=duration).save()
        return success()
    except Exception as e:
        return error(e)

@csrf_exempt 
@api_view(['POST'])
def add_stream(request):
    if request.user.has_perm('streams.add_streams'):
        course_id = request.POST.get('course_id')
        stream_name = request.POST.get('stream_name')
        try:
            Streams(course_id_id=course_id, stream_name=stream_name).save()
            return success("Stream added sucessfully.")
        except Exception as e:
            return error(e)
    else:
        return error("")

@csrf_exempt
@api_view(['POST'])
def add_subject(request):
    subject_name = request.POST.get('subject_name')
    semester = request.POST.get('semester')
    stream_id = request.POST.get('stream_id')
    try:
        Subjects(stream_id_id=stream_id, subject_name=subject_name, semester=semester).save()
        return success()
    except Exception as e:
        return error(e)

# @api_view(['GET'])  
def get_all_course(request):
    temp = []
    course_data = Courses.objects.all()
    for course in course_data:
        all_streams = [str(stream[0]) for stream in Streams.objects.filter(course_id=course.id).values_list('stream_name')]
        temp.append({"id": course.id, "course_name": course.course_name, "duration": course.duration, 'streams': all_streams})

    return success(temp)

@api_view(['GET'])
def get_all_streams_by_course_id(request):
    course_id = request.GET.get('course_id')
    streams_data = Streams.objects.filter(id=course_id)     
    data = [{"stream_name": stream.stream_name, "stream_id": stream.stream_id} for stream in streams_data]
    if not data:
        return success("Course not availabe with course id '{}'".format(course_id))
    return success(data)

@csrf_exempt
def generate_token(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            user = auth.authenticate(username=username, password=password)
            if user:
                key = CustomToken.objects.create(user=(User.objects.get(username=user)), expires_time = time.time() + 86400)
                return success({"access_token": key.key})
            return error("Incorrect Password")
        return error("Username is not registered")
    return error("GET method not allowed")
