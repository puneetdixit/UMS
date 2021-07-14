from django.urls import path

from . import views

urlpatterns = [
    # path('get_student_data', views.get_student_data, name='get_student_data'),
    path('add_subject', views.add_subject, name='add_subject'),
    path('add_course', views.add_course, name='add_course'),
    path('add_stream', views.add_stream, name='add_stream'),
    path('get_all_course', views.get_all_course, name='get_all_course'),
    path('get_all_streams_by_course_id', views.get_all_streams_by_course_id, name='get_all_streams_by_course_id'),
    path('generate_token', views.generate_token, name='generate_token'),
]
