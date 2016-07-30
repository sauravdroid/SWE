from django.shortcuts import render
from django.http import HttpResponse
from .forms import *
from .redirect import *
from . import status
from . import designation
from django.contrib.auth import login, logout, authenticate
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from django.utils import timezone
from django.db.utils import IntegrityError
from . import host_email
from django.views import generic


# Create your views here.
def index(request):
    if request.method == 'POST':
        form = UserFormMain(request.POST)
        form1 = UserFormMain(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            return HttpResponse("Successful")
    else:
        form = TeacherForm()
        form1 = UserFormMain()

    return render(request, 'User/user_register.html', {"form": form, "form1": form1})


def user_main_register(request):
    if request.method == 'GET':
        form = UserFormMain()
        return render(request, 'User/user_main_registration.html', {"form": form})

    return HttpResponse("Null")


def login_user(request):
    if request.user.is_authenticated():
        if request.user.is_admin:
            return redirect('user:controller_profile')
        else:
            return redirect('user:user_profile')
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        if request.GET.get('next'):
                            return redirect(request.GET.get('next'))
                        if request.user.is_admin:
                            return redirect('user:controller_profile')
                        else:
                            return redirect('user:user_profile')
                else:
                    return HttpResponse("Wrong username or password")
        else:
            form = LoginForm()
        return render(request, "User/login.html", {"form": form, "button_text": 'Login', 'title': "Login"})


def logout_user(request):
    logout(request)
    return redirect('user:login')


def controller_profile(request):
    if check_superuser(request):
        departments = Department.objects.all().count()
        courses = Course.objects.all().count()
        subjects = Subject.objects.all().count()
        challans = Challan.objects.all().count()
        students = StudentDetail.objects.all().count()
        question_papers = QuestionPaper.objects.all().count()
        return render(request, 'User/controller-profile.html', {'paper_setter': status.paper_setter,
                                                                'moderator': status.moderator,
                                                                'examiner': status.examiner,
                                                                'scrutinizer': status.scrutinizer,
                                                                'head_examiner': status.head_examiner,
                                                                'departments': departments,
                                                                'courses': courses,
                                                                'subjects': subjects,
                                                                'challans': challans,
                                                                'students': students,
                                                                'question_papers': question_papers})
    return HttpResponse("You don't have sufficient permission to view this page")


def register_teacher(request):
    if check_superuser(request):
        if request.method == 'GET':
            form = UserFormMain()
            return render(request, 'User/login.html',
                          {"form": form, "button_text": "Register", "title": "Registration"})
        else:
            form = UserFormMain(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                password = form.cleaned_data['password']
                user.set_password(password)
                user.save()
                send_mail_to_user(form.cleaned_data['username'], password, host_email.email)
                return HttpResponse("Successfully Registered " + form.cleaned_data['email'])
    else:
        return HttpResponse("You have to login as the controller.You don't have sufficient permission")


def send_email(request):
    username = 'sauravdroid16'
    password = 'terikyasgo'
    send_mail(
        'Activating your account',
        'Please to go to this link to activate your account -> http://localhost:8000/user/controller/ username: ' + username + " ,password: " + password,
        'saru.sreyo@gmail.com',
        ['sauravdroid16@gmail.com'],
        fail_silently=False,
    )
    return HttpResponse("Maill sent successfully")


def check_superuser(req):
    superuser = False
    if req.user.is_authenticated() and req.user.is_admin:
        superuser = True
    return superuser


def send_mail_to_user(username, password, email):
    send_mail(
        'Activating your account',
        'Please to go to this link to activate your account -> http://localhost:8000/user/activate_account/ username: ' + username + " ,password: " + password,
        'saru.sreyo@gmail.com',
        [email],
        fail_silently=False,
    )
    return HttpResponse("Maill sent successfully")


@login_required(login_url='user:login')
def user_profile(request):
    if request.user.is_admin:
        return render(request, 'User/controller-profile.html', {})
    else:
        designation = request.user.designation
        if designation == 'student':
            return render(request, 'User/student_profile.html', {'user': request.user})
        else:  # For all other user except students
            try:
                one_to_one_field = request.user.userstaff
            except ObjectDoesNotExist:
                return HttpResponse("You must activate your account from the mail sent by the user")

            try:
                appointed = one_to_one_field.appointment_set.get(user=one_to_one_field)
                role = ' '.join(appointed.role.upper().split('_'))
                role_raw = appointed.role
                role_status = appointed.status
                is_appointed = "true"
                '''return render(request, 'User/user_profile.html', {"designation": designation.upper(),
                                                                  "role": role, "status": role_status,"appointed":"true"})'''
            except ObjectDoesNotExist:
                role = "Not Appointed"
                role_status = "None"
                role_raw = "not_appointed"
                is_appointed = "false"
                '''return render(request, 'User/user_profile.html', {"designation": designation.upper(),
                                                                  "role": "Not Appointed", "status": "none","appointed":"false"})'''
            return render(request, 'User/user_profile.html',
                          {"username": request.user.username, "designation": designation.upper(),
                           "role": role, "status": role_status,
                           "appointed": is_appointed, "role_raw": role_raw})


@login_required(login_url='user:login')
def user_activation(request):
    if request.method == "GET":
        if request.user.is_admin:
            return redirect('user:controller_profile')
        else:
            try:
                one_to_one_field = request.user.userstaff
                return HttpResponse("You have already alreay activated your account")
            except ObjectDoesNotExist:
                form = TeacherForm()
                return render(request, 'User/user_activation.html', {"form": form, "username": request.user.username})
    else:
        form = TeacherForm(request.POST)
        if form.is_valid():
            user_data = form.save(commit=False)
            user_data.user = request.user
            user_data.is_activated = True
            user_data.save()
            if user_data.user.designation == 'hod':
                try:
                    hod = HOD(department=user_data.department_fk, user=request.user.userstaff,
                              date_of_appointment=timezone.now())
                    hod.save()
                except IntegrityError as e:
                    request.user.userstaff.delete()
                    return HttpResponse("A Hod already exists for this department")
            return redirect('user:user_profile')


@login_required(login_url='user_login')
def create_department(request):
    if check_superuser(request):
        if request.method == "GET":
            form = CreateDepartmentForm()
            return render(request, 'User/create_actions.html',
                          {"form": form, "button_text": "Create Department", "title": "Department"})
        else:
            form = CreateDepartmentForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                raw_data = form.cleaned_data['department_name']
                processed_department_name = ''.join(raw_data.lower().split())
                user.department_name = processed_department_name
                user.dept_name = raw_data.upper()
                user.save()
                return HttpResponse("Successfully Created Department")
    else:
        return permission_error()


@login_required(login_url='user:login')
def create_course(request):
    if check_superuser(request):
        if request.method == 'GET':
            form = CreateCourseForm()
            return render(request, 'User/create_actions.html',
                          {"form": form, "button_text": "Create Course", "title": "Course"})
        else:
            form = CreateCourseForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                raw_data = form.cleaned_data['name']
                processed_name = ''.join(raw_data.lower().split())
                user.name = processed_name
                user.name_new = raw_data.upper()
                user.save()
                return HttpResponse("Course successfully created.")
    else:
        return permission_error()


@login_required(login_url='user:login')
def set_hod(request):
    if check_superuser(request):
        if request.method == "GET":
            hods = CustomUser.objects.filter(designation=designation.hod)
            form = SetHodForm()
            return render(request, 'User/set_hod.html', {"hods": hods, "form": form})
        else:
            form = SetHodForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                hod = CustomUser.objects.get(username=request.POST.get('hod')).userstaff
                user.user = hod
                user.save()
                return HttpResponse("Successfully designated H.O.D")
            hod = request.POST.get('hod')
    else:
        return permission_error()


@login_required(login_url='user:login')
def create_subject(request):
    if request.method == "GET":
        form = CreateSubjectForm()
        return render(request, 'User/create_actions.html',
                      {"form": form, "button_text": "Create Subject", "title": "Subject"})
    else:
        form = CreateSubjectForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_name = form.cleaned_data['name']
            processed_name = ''.join(raw_name.lower().split())
            course_name = raw_name.upper()
            code = ''.join(form.cleaned_data['code'].upper().split())
            user.name = processed_name
            user.name_new = course_name
            user.code = code
            user.save()
            return HttpResponse("Successfully created subject")


@login_required(login_url='user:login')
def send_appointment_paper_setter(request, role):
    if check_superuser(request):
        form = SendAppointmentForm()
        subjects = Subject.objects.all()
        if request.method == "GET":
            return render(request, 'User/send_appointment.html', {"form": form, "role": role, "subjects": subjects})
        else:
            if role == status.paper_setter:
                subject_code = request.POST.get('subject')
                subject = Subject.objects.get(code=subject_code)
                form = SendAppointmentForm(request.POST, request.FILES)
                if form.is_valid():
                    appointment = form.save(commit=False)
                    if appointment.user.department_fk == subject.course.department:
                        appointment.role = role
                        appointment.status = status.pending
                        appointment.appointment_username = appointment.user.user.username
                        appointment.year_of_appointment = appointment.appoimtment_termination_date.year
                        # Updating the PaperSetter Model
                        paper_setter = PaperSetter(setter=appointment.user, subject=subject)
                        paper_setter.setter_user_name = appointment.user.user.username
                        paper_setter.appointment_year = appointment.appoimtment_termination_date.year
                        paper_setter.subject_name = paper_setter.subject.name_new
                        appointment.save()
                        paper_setter.save()
                        return HttpResponse("Appointment Sent")
                    else:
                        return render(request, 'User/send_appointment.html',
                                      {"form": form, "role": role, "subjects": subjects,
                                       "error_message": "Subject department should be same as the Paper Setter department"})
                        # return HttpResponse(subject.name)
            else:
                form = SendAppointmentForm(request.POST)
                if form.is_valid():
                    appointment = form.save(commit=False)
                    appointment.role = role
                    appointment.status = status.pending
                    appointment.appointment_username = appointment.user.user.username
                    appointment.year_of_appointment = appointment.appoimtment_termination_date.year
                    appointment.save()
                    return HttpResponse("Appointment Sent")
    else:
        return permission_error()


@login_required(login_url='user:login')
def approve_appointment(request, role):
    if request.method == 'GET':
        appointment = request.user.userstaff.appointment_set.get(user=request.user.userstaff)
        if role == status.paper_setter:
            subject = request.user.userstaff.papersetter_set.get(setter=request.user.userstaff).subject
            return render(request, 'User/approve_appointment.html', {"appointment": appointment, "subject": subject,
                                                                     "role": role})
        elif role == status.moderator:
            course = request.user.userstaff.moderator_set.get(user=request.user.userstaff).course
            return render(request, 'User/approve_appointment.html', {"appointment": appointment, "course": course,
                                                                     "role": role})
    else:
        if role == status.paper_setter:
            paper_setter = request.user.userstaff.papersetter_set.get(setter=request.user.userstaff)
            paper_setter.status = status.accepted
            paper_setter.date_of_appointment = timezone.now()
            paper_setter.save()
        else:
            moderator = request.user.userstaff.moderator_set.get(user=request.user.userstaff)
            moderator.status = status.accepted
            moderator.date_of_appointment = timezone.now()
            moderator.save()
        appointment_obj = request.user.userstaff.appointment_set.get(user=request.user.userstaff)
        appointment_obj.status = status.accepted
        appointment_obj.save()
        return HttpResponse("Approved")


@login_required(login_url='user:login')
def make_questionpaper(request):
    if request.method == "GET":
        form = MakeQuestionPaperForm()
        return render(request, 'User/upload_questionpaper.html', {"form": form})
    else:
        form = MakeQuestionPaperForm(request.POST, request.FILES)
        if form.is_valid():
            question_paper = form.save(commit=False)
            subject = request.user.userstaff.papersetter_set.get(setter=request.user.userstaff).subject
            paper_setter = request.user.userstaff.papersetter_set.get(setter=request.user.userstaff)
            question_paper.subject = subject
            question_paper.paper_setter = paper_setter
            question_paper.subject_name = subject.name
            question_paper.course = subject.course
            question_paper.save()
            return HttpResponse("Forwarded to moderator")
    return HttpResponse("Make Question Paper")


@login_required(login_url='user:login')
def send_appointment_moderator(request):
    form = SendAppointmentForm()
    courses = Course.objects.all()
    if request.method == 'GET':
        return render(request, 'User/send_appointment.html', {"form": form, "courses": courses, "role": "moderator"})
    else:
        course_name = request.POST.get('course')
        course = Course.objects.get(name=course_name)
        form = SendAppointmentForm(request.POST, request.FILES)
        if form.is_valid():
            appointment = form.save(commit=False)
            if appointment.user.department_fk == course.department:
                moderator = Moderator(user=appointment.user, course=course)
                appointment.role = status.moderator
                appointment.appointment_username = appointment.user.user.username
                appointment.year_of_appointment = appointment.appoimtment_termination_date.year
                moderator.moderator_username = appointment.user.user.username
                moderator.appointment_year = appointment.appoimtment_termination_date.year
                moderator.save()
                appointment.save()
                return HttpResponse("Appointment Sent")
            else:
                return render(request, 'User/send_appointment.html',
                              {"form": form, "courses": courses, "role": "moderator",
                               "error_message": "Subject department should be same as the Paper Setter department"})
    return HttpResponse("Error occured.Please ensure that all fields are filled")


@login_required(login_url='user:login')
def confirm_questionpaper(request):
    form = ConfirmQuestionPaperForm()
    course = request.user.userstaff.moderator_set.get(user=request.user.userstaff).course
    question_papers = QuestionPaper.objects.filter(course=course, approved=False)
    if request.method == 'GET':
        return render(request, 'User/confirming_questionpaper_moderator.html', {"form": form,
                                                                                "question_papers": question_papers})
    else:
        question_paper_id = request.POST.get('question_paper_id')
        question_paper = QuestionPaper.objects.get(pk=question_paper_id)
        question_paper.approval_date = timezone.now()
        question_paper.full_marks = request.POST.get('full_marks')
        question_paper.time = request.POST.get('duration')
        question_paper.year_of_examination = request.POST.get('year')
        question_paper.save()
        return render(request, 'User/confirming_questionpaper_moderator.html', {"form": form,
                                                                                "question_papers": question_papers,
                                                                                "message": "Approval Successful"})


@login_required(login_url='user:login')
def upload_schedule(request):
    if request.user.designation == 'hod':
        courses = request.user.userstaff.department_fk.course_set.all()
        return render(request, 'User/upload_schedule_courses.html', {"courses": courses})
    else:
        return HttpResponse("You don't have permssion to view this page")


def permission_error():
    return HttpResponse("You don't have sufficient permission to view this page ")


@login_required(login_url='user:login')
def upload_schedule_course(request, course):
    if request.user.designation == 'hod':
        if request.method == 'GET':
            form = UploadScheduleForm()
            return render(request, 'User/upload_schedule.html', {"form": form, "course": course})
        else:
            form = UploadScheduleForm(request.POST, request.FILES)
            course = Course.objects.get(name=course)
            if form.is_valid():
                try:
                    schedule = form.save(commit=False)
                    schedule.course = course
                    schedule.save()
                    return HttpResponse("Schedule Uploaded")
                except IntegrityError as e:
                    schedule = Timetable.objects.get(course=course)
                    schedule.timetable_file = form.cleaned_data['timetable_file']
                    schedule.date_uploaded = timezone.now()
                    schedule.save()
                    return HttpResponse("Schedule Updated")
    else:
        return permission_error()


@login_required(login_url='user:login')
def create_challan(request, course):
    if check_superuser(request):
        if request.method == 'GET':
            form = CreateChallanForm()
            course = Course.objects.get(name=course)
            return render(request, 'User/create_challan.html', {"form": form, "course": course})
        else:
            course_obj = Course.objects.get(name=course)
            form = CreateChallanForm(request.POST)
            if form.is_valid():
                challan = form.save(commit=False)
                challan.course = course_obj
                challan.course_name = course
                challan.save()
            return HttpResponse("Challan Created")
    else:
        return permission_error()


@login_required(login_url='user:login')
def show_course_challan(request):
    if check_superuser(request):
        courses = Course.objects.all()
        return render(request, 'User/challan_course_list.html', {"courses": courses})
    else:
        return permission_error()


def register_student(request):
    if request.method == 'GET':
        custom_user_form = StudentCustomUserForm()
        student_detail_form = RegisterStudentForm()
        return render(request, 'User/register_student.html',
                      {"custom_user_form": custom_user_form, "student_detail_form": student_detail_form})
    else:
        custom_user_form = StudentCustomUserForm(request.POST)
        student_detail_form = RegisterStudentForm(request.POST)
        if custom_user_form.is_valid() and student_detail_form.is_valid():
            custom_user = custom_user_form.save(commit=False)
            password = custom_user_form.cleaned_data['password']
            custom_user.set_password(password)
            custom_user.designation = "student"
            student_detail = student_detail_form.save(commit=False)
            try:
                challan = Challan.objects.get(course_name=student_detail.course_taken.name,
                                              semester=student_detail.semester)
            except ObjectDoesNotExist:
                return HttpResponse("No Challan for this Course or Subject yet")
            custom_user.save()
            student_detail.student = custom_user
            student_detail.roll = StudentDetail.objects.all().count() + 1
            student_detail.save()
            request.session['registration_id'] = student_detail.registration_id
            return redirect('user:challan_payment', course=student_detail.course_taken.name,
                            semester=student_detail.semester)
        return HttpResponse("Error Occured")


def challan_payment(request, course, semester):
    if request.method == "GET":
        challan = Challan.objects.get(course_name=course, semester=semester)
        registration_id = request.session.get('registration_id', False)
        return render(request, 'User/student_challan_payment.html',
                      {"challan": challan, "registration_id": registration_id})
    else:
        student = StudentDetail.objects.get(registration_id=request.POST.get('registration_id'))
        student.paid = True
        student.save()
        request.session.clear()
        return HttpResponse("Payment Successful")


@login_required(login_url='user:login')
def download_admit_card(request):
    if request.user.designation == 'student':
        return render(request, 'User/download_admit_card.html',
                      {"user": request.user, "detail": request.user.studentdetail})
    else:
        return permission_error()


@login_required(login_url='user:login')
def download_challan(request):
    challan = Challan.objects.get(course=request.user.studentdetail.course_taken,
                                  semester=request.user.studentdetail.semester)
    return render(request, 'User/download_challan.html', {"user": request.user, "challan": challan})


def approve_div(request):
    return render(request, 'User/table.html', {})


def DepartmentList(request, model):
    if request.method == "GET":
        if model == 'Department':
            results = Department.objects.all()
            return render(request, 'User/listview_list.html', {"departments": results, 'model': model})
        elif model == 'Subject':
            results = Subject.objects.all()
            return render(request, 'User/listview_list.html', {"departments": results, 'model': model})
        elif model == 'Course':
            results = Course.objects.all()
            return render(request, 'User/listview_list.html', {"departments": results, 'model': model})

        elif model == 'Challan':
            results = Challan.objects.all()
            return render(request, 'User/listview_list.html', {"departments": results, 'model': model})

        elif model == 'Student':
            results = StudentDetail.objects.all()
            return render(request, 'User/listview_list.html', {"departments": results, 'model': model})

        elif model == 'QuestionPaper':
            results = QuestionPaper.objects.all()
            return render(request, 'User/listview_list.html', {"departments": results, 'model': model})

        elif model == 'Teacher':
            results = UserStaff.objects.filter(user__designation='teacher')
            return render(request, 'User/listview_list.html', {"departments": results, 'model': model})

        elif model == 'Moderator':
            results = Moderator.objects.all()
            return render(request, 'User/listview_list.html', {"departments": results, 'model': model})

        elif model == 'PaperSetter':
            results = PaperSetter.objects.all()
            return render(request, 'User/listview_list.html', {"departments": results, 'model': model})

        elif model == 'TimeTable':
            results = Timetable.objects.all()
            return render(request, 'User/listview_list.html', {"departments": results, 'model': model})
    else:
        subject_name = request.POST.get('subject_name')
        question_paper = QuestionPaper.objects.get(subject_name=subject_name)
        question_paper.approved = True
        question_paper.approval_date = timezone.now()
        question_paper.save()
        return HttpResponse("Approved")


class DepartmentDetail(generic.DetailView):
    context_object_name = 'department'
    model = Department
    template_name = 'User/detail-view.html'
