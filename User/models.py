from __future__ import unicode_literals
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
from django.db import models
from django.conf import settings
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, email, first_name, last_name):
        if not email:
            raise ValueError("You must specify a valid email ! ")
        user = self.model(
            email=self.normalize_email(email),
            password=password,
            first_name=last_name,
            last_name=last_name,
            username=username
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password, first_name, last_name):
        user = self.create_user(email=email, username=username, password=password, first_name=first_name,
                                last_name=last_name)
        user.is_admin = True
        user.save()
        return user


class CustomUser(AbstractBaseUser):
    designation_choices = (
        ('hod', 'H.O.D'), ('teacher', 'Teacher'),)
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    designation = models.CharField(max_length=255, choices=designation_choices)
    objects = CustomUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'CustomUser'

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.username + " / " + self.designation

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Department(models.Model):
    group_choices = (('ag', 'Agriculture'), ('arts', 'Arts'), ('commerce', 'Commerce'),
                     ('education', 'Education, Journalism & Library Science'), ('engg', 'Engineering & Technology'),
                     ('arts', 'Fine Arts, Music and Home Science'), ('Law', 'Law'))
    location_choices = (
        ('rb', 'Rajabazar'), ('sl', 'Saltlake'), ('h', 'Hazra'), ('cs', 'College Street'), ('b', 'Ballygunje'))
    location = models.CharField(max_length=255, choices=location_choices)
    department_name = models.CharField(max_length=255, unique=True)
    group = models.CharField(max_length=100, choices=group_choices, default='engg')
    dept_name = models.CharField(max_length=255)

    def __str__(self):
        return self.dept_name

    def get_field_values(self):
        return [field.value_to_string(self) for field in Department._meta.fields]




class UserStaff(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.TextField()
    year_of_join = models.DateField()
    department_fk = models.ForeignKey(Department)
    # department_id = models.CharField(max_length=20)
    # designation = models.CharField(max_length=255)
    is_activated = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " ( " + self.department_fk.dept_name + " ) "


class Course(models.Model):
    course_choice = (('commerce', 'M.Com'), ('business', 'M.Bm'), ('doctorate', 'Ph.D'),
                     ('education', 'M.Ed'), ('post-doctoral', 'M.Phil'), ('science', 'M.Sc'),
                     ('tech', 'M.Tech'),)
    name = models.CharField(max_length=255, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    course = models.CharField("Award", max_length=255, choices=course_choice)
    name_new = models.CharField(max_length=255)
    challan_created = models.BooleanField(default=False)

    def __str__(self):
        return self.name_new + " (" + self.department.dept_name + ") "


class HOD(models.Model):
    department = models.OneToOneField(Department, on_delete=models.CASCADE)
    user = models.OneToOneField(UserStaff, on_delete=models.CASCADE)
    date_of_appointment = models.DateField(default=timezone.now())

    def __str__(self):
        return self.user.user.username + " ->" + self.department.dept_name


class Subject(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20, unique=True)
    course = models.ForeignKey(Course)
    name_new = models.CharField(max_length=255)
    semester = models.IntegerField(default=1)

    def __str__(self):
        return self.name_new + " --> " + self.code + " --> " + self.course.name + " --> " + self.course.department.department_name


class PaperSetter(models.Model):
    status_choices = (('accepted', 'Accepted'), ('rejected', 'Rejected'), ('pending', 'Pending'))
    setter = models.ForeignKey(UserStaff, on_delete=models.CASCADE)
    setter_user_name = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject)
    subject_name = models.CharField(max_length=255)
    date_of_appointment = models.DateField(null=True)
    status = models.CharField(max_length=20, choices=status_choices, default="pending")
    appointment_year = models.IntegerField(default=2016)

    class Meta:
        unique_together = (('setter_user_name', 'appointment_year'))

    def __str__(self):
        return self.setter.user.username + " --> " + self.subject.name_new + " --> " + self.status


class Moderator(models.Model):
    status_choices = (('accepted', 'Accepted'), ('rejected', 'Rejected'), ('pending', 'Pending'))
    user = models.ForeignKey(UserStaff, on_delete=models.CASCADE)
    moderator_username = models.CharField(max_length=255)
    course = models.OneToOneField(Course, on_delete=models.CASCADE)
    date_of_appointment = models.DateField(default=timezone.now())
    status = models.CharField(max_length=20, choices=status_choices, default="pending")
    appointment_year = models.IntegerField(default=2016)

    class Meta:
        unique_together = (('moderator_username', 'appointment_year'),)

    def __str__(self):
        return self.user.user.username + " --> " + self.course.name_new + "-->" + self.status


class Appointment(models.Model):
    status_choices = (('accepted', 'Accepted'), ('rejected', 'Rejected'), ('pending', 'Pending'))
    role_choices = (('paper_setter', 'Paper Setter'), ('moderator', 'Moderator'), ('examiner', 'Examiner'),
                    ('scrutinizer', 'Scrutinizer'), ('head_examiner', 'Head Examiner'),)
    user = models.ForeignKey(UserStaff, unique=True)
    appointment_username = models.CharField(max_length=255)
    role = models.CharField(max_length=30, choices=role_choices)
    date_sent = models.DateField(default=timezone.now())
    appoimtment_termination_date = models.DateField()
    status = models.CharField(max_length=20, choices=status_choices, default="pending")
    appointment_file = models.FileField()
    year_of_appointment = models.IntegerField(default=2016)

    class Meta:
        unique_together = (('appointment_username', 'year_of_appointment'),)

    def __str__(self):
        return self.user.user.username + " -- " + self.role + " -- " + self.status


class QuestionPaper(models.Model):
    paper = models.FileField(null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    subject_name = models.CharField(max_length=255)
    paper_setter = models.ForeignKey(PaperSetter)
    course = models.ForeignKey(Course)
    approved = models.BooleanField(default=False)
    approval_date = models.DateField(null=True)
    full_marks = models.IntegerField(default=0)
    time = models.CharField(default="3", max_length=2)
    year_of_examination = models.IntegerField(default=2016)

    class Meta:
        unique_together = (('subject_name', 'year_of_examination'),)

    def __str__(self):
        return self.subject.name_new + " --> " + self.subject.course.name_new


class Timetable(models.Model):
    timetable_file = models.FileField(null=True, blank=True)
    course = models.OneToOneField(Course, on_delete=models.CASCADE)
    date_uploaded = models.DateField(default=timezone.now())
    is_approved = models.BooleanField(default=True)

    def __str__(self):
        return self.course.name_new


class StudentDetail(models.Model):
    student = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    roll = models.CharField(max_length=5)
    registration_id = models.CharField(max_length=20, unique=True)
    course_taken = models.ForeignKey(Course)
    semester = models.IntegerField(max_length=5)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.student.get_full_name()


class Challan(models.Model):
    course = models.ForeignKey(Course)
    course_name = models.CharField(max_length=255)
    semester = models.IntegerField(max_length=5)
    application_form_cost = models.IntegerField("Cost of Application Form", default=0)
    examination_fess_th = models.IntegerField("Examination fees for Theoretical papers", default=0)
    examination_fess_pr = models.IntegerField("Examination fees for Practical papers", default=0)
    centre_fees = models.IntegerField(default=0)

    class Meta:
        unique_together = (('course_name', 'semester'),)

    def __str__(self):
        return self.course.name_new + " Total Fees --> " + str(self.get_total_form_cost()) \
               + " Semester -- >" + str(self.semester)

    def get_total_form_cost(self):
        return self.application_form_cost + self.examination_fess_pr + self.examination_fess_th + self.centre_fees
