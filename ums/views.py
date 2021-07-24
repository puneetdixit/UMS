from django.contrib.auth.models import auth
from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from ums.models import *


def error(err):
    return JsonResponse({"status": "failure", "desc": str(err)})


def success(data=None, additional_data=None):
    output_data = {"status": "success", "data": data if data else True}
    if additional_data:
        output_data.update(additional_data)
    return JsonResponse(output_data)


@csrf_exempt
@api_view(['POST'])
def add_course(request):
    course_name = request.POST.get('course_name')
    duration = request.POST.get('duration')
    try:
        course = Courses(course_name=course_name, duration=duration)
        course.save()
        return success({"course_id": course.id})
    except Exception as e:
        return error(e)


@csrf_exempt
@api_view(['POST'])
def add_stream(request):
    if request.user.has_perms('streams.add_streams'): # permission check for user to add data in streams.
        course_id = request.POST.get('course_id')
        stream_name = request.POST.get('stream_name')
        if Courses.objects.filter(id=course_id).exists():
            try:
                stream = Streams(course_id_id=course_id, stream_name=stream_name)
                stream.save()
                return success({"stream_id": stream.id})
            except Exception as e:
                return error(e)
        return error("Course id {} not found".format(course_id))
    else:
        return error("Permission Denied")


@csrf_exempt
@api_view(['DELETE', 'POST'])
def delete_stream(request):
    if request.user.has_perms('streams.delete_streams') or request.user.is_admin:
        stream_id = request.POST.get('stream_id')
        if Streams.objects.filter(id=stream_id).exists():
            Subjects.objects.filter(stream_id=stream_id).delete()
            Streams.objects.filter(id=stream_id).delete()
            return success() 
        return error("Stream id {} not found".format(stream_id))
    return error("Permission Denied")


@csrf_exempt
@api_view(['POST'])
def add_subject(request):
    if request.user.is_admin or request.user.has_perms('subjects.add_subjects'):
        subject_name = request.POST.get('subject_name')
        semester = request.POST.get('semester')
        stream_id = request.POST.get('stream_id')
        try:
            Subjects(stream_id_id=stream_id, subject_name=subject_name, semester=semester).save()
            return success()
        except Exception as e:
            return error(e)
    return error("Permission Denied")


@api_view(['GET'])
def get_all_course(request):
    data = []
    course_data = Courses.objects.all()
    for course in course_data:
        all_streams = {stream.id: stream.stream_name for stream in Streams.objects.filter(course_id= course.id)}
        data.append(
            {"id": course.id, "course_name": course.course_name, "duration": course.duration, 'streams': all_streams})
    return success(data)


@api_view(['GET'])
def get_all_streams_by_course_id(request):
    course_id = request.GET.get('course_id')
    streams_data = Streams.objects.filter(course_id_id=course_id)
    print("streams_data", streams_data)
    data = [{"stream_name": stream.stream_name, "stream_id": stream.id} for stream in streams_data]
    if not data:
        return success("Course not available with course id '{}'".format(course_id))
    return success(data)


@csrf_exempt
def generate_token(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            user = auth.authenticate(username=username, password=password)
            if user:
                key = CustomToken.objects.create(user=(User.objects.get(username=user)),
                                                 expires_time=time.time() + 86400)
                return success({"access_token": key.key})
            return error("Incorrect Password")
        return error("Incorrect / Unregistered Username : {}".format(username))
    return error("GET method not allowed")
