from django.conf.urls import url
from . import views
from . import views_serializer
from rest_framework.urlpatterns import format_suffix_patterns
app_name = 'user'

urlpatterns = [
    url(r'^$', views.login_user, name='login'),
    url(r'^main_register/$', views.user_main_register, name='main_register'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^controller/$', views.controller_profile, name='controller_profile'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^register/$', views.register_teacher, name='register_teacher'),
    url(r'^send_mail/$', views.send_email, name='send_email'),
    url(r'^profile/$', views.user_profile, name='user_profile'),
    url(r'^activate_account/$', views.user_activation, name='user_activation'),
    url(r'^create_department/$', views.create_department, name='create_department'),
    url(r'^create_course/$', views.create_course, name='create_course'),
    url(r'^create_subject/$', views.create_subject, name='create_subject'),
    url(r'^set_hod/$', views.set_hod, name='set_hod'),
    url(r'^send_appointment_setter/(?P<role>[\w.@\-]+)/', views.send_appointment_paper_setter,
        name='send_appointment_setter'),
    url(r'^approve_appointment/(?P<role>[\w.@\-]+)/$', views.approve_appointment, name='approve_appointment'),
    url(r'^make_questionpaper/$', views.make_questionpaper, name='make_questionpaper'),
    url(r'^send_appointment_moderator/$', views.send_appointment_moderator, name='send_appointment_moderator'),
    url(r'^confirm_questionpaper/$', views.confirm_questionpaper, name='confirm_questionpaper'),
    url(r'^upload_schedule/$', views.upload_schedule, name='upload_schedule'),
    url(r'^upload_schedule_course/(?P<course>[\w.@\-]+)/$', views.upload_schedule_course,
        name='upload_schedule_course'),
    url(r'^create_challan/(?P<course>[\w.@\-]+)/$', views.create_challan, name='create_challan'),
    url(r'^show_course_challan/$', views.show_course_challan, name='show_course_challan'),
    url(r'^register_student/$', views.register_student, name='register_student'),
    url(r'^challan_payment/(?P<course>[\w.@\-]+)/(?P<semester>[0-9]+)/$', views.challan_payment,
        name='challan_payment'),
    url(r'^download_admit_card/$', views.download_admit_card, name='download_admit_card'),
    url(r'^download_challan/$', views.download_challan, name='download_challan'),
    url(r'^approve_div/$', views.approve_div, name='approve_div'),
    url(r'^detail_list/(?P<model>[\w.@\-]+)/$', views.DepartmentList,name='detail_list'),
    url(r'^department_detail/(?P<pk>[0-9]+)/$', views.DepartmentDetail.as_view(),name='department_detail'),
    url(r'^serialize/$', views_serializer.CustomUserList.as_view(),name='department_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)