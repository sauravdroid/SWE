from django import forms
from .models import *


class TeacherForm(forms.ModelForm):
    class Meta:
        model = UserStaff
        exclude = ['user', 'is_activated']


class UserFormMain(forms.ModelForm):
    email = forms.CharField(label='Email',
                            widget=forms.EmailInput(attrs={'class': 'mdl-textfield__input', 'autocomplete': 'off'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'mdl-textfield__input'}))
    username = forms.CharField(label='Username',
                               widget=forms.TextInput(attrs={'class': 'mdl-textfield__input', 'autocomplete': 'off'}))
    first_name = forms.CharField(label='First Name',
                                 widget=forms.TextInput(attrs={'class': 'mdl-textfield__input', 'autocomplete': 'off'}))
    last_name = forms.CharField(label='Last Name',
                                widget=forms.TextInput(attrs={'class': 'mdl-textfield__input', 'autocomplete': 'off'}))

    class Meta:
        model = CustomUser
        exclude = ['is_active', 'is_admin', 'last_login']


class LoginForm(forms.Form):
    username = forms.CharField(label='Username',
                               widget=forms.TextInput(attrs={'class': 'mdl-textfield__input', 'autocomplete': 'off'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'mdl-textfield__input'}))


class CreateDepartmentForm(forms.ModelForm):
    department_name = forms.CharField(label='Department Name', widget=forms.TextInput(
        attrs={'class': 'form-text-field'}
    ))

    class Meta:
        model = Department
        # fields ='__all__'
        exclude = ['dept_name']


class CreateCourseForm(forms.ModelForm):
    name = forms.CharField(label='Course Name', widget=forms.TextInput(
        attrs={'class': 'form-text-field'}
    ))

    class Meta:
        model = Course
        # fields = '__all__'
        exclude = ['name_new', 'challan_created']


class SetHodForm(forms.ModelForm):
    class Meta:
        model = HOD
        exclude = ['user']


class CreateSubjectForm(forms.ModelForm):
    name = forms.CharField(label='Subject Name', widget=forms.TextInput(
        attrs={'class': 'form-text-field'}
    ))
    code = forms.CharField(label='Subject Code', widget=forms.TextInput(
        attrs={'class': 'form-text-field'}
    ))
    semester = forms.CharField(label='Semester', widget=forms.TextInput(
        attrs={'class': 'form-text-field'}
    ))

    class Meta:
        model = Subject
        exclude = ['name_new']


class SendAppointmentForm(forms.ModelForm, forms.Form):
    appoimtment_termination_date = forms.CharField(label='Department Name', widget=forms.TextInput(
        attrs={'class': 'form-text-field'}
    ))

    class Meta:
        model = Appointment
        exclude = ['date_sent', 'status', 'role', 'appointment_username', 'year_of_appointment']


class MakeQuestionPaperForm(forms.ModelForm):
    class Meta:
        model = QuestionPaper
        fields = ['paper', 'year_of_examination']


class ConfirmQuestionPaperForm(forms.ModelForm):
    class Meta:
        model = QuestionPaper
        fields = ['full_marks', 'time', 'year_of_examination']


class UploadScheduleForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = ['timetable_file']


class CreateChallanForm(forms.ModelForm):
    semester = forms.CharField(label='Semester',
                               widget=forms.NumberInput(attrs={'class': 'mdl-textfield__input', 'autocomplete': 'on'}))
    application_form_cost = forms.CharField(label='Application form Cst',
                                            widget=forms.NumberInput(
                                                attrs={'class': 'mdl-textfield__input', 'autocomplete': 'on'}))
    examination_fess_th = forms.CharField(label='Theory paper Examination Cost',
                                          widget=forms.NumberInput(
                                              attrs={'class': 'mdl-textfield__input', 'autocomplete': 'on'}))

    examination_fess_pr = forms.CharField(label='Practical paper Examination Cost',
                                          widget=forms.NumberInput(
                                              attrs={'class': 'mdl-textfield__input', 'autocomplete': 'on'}))

    centre_fees = forms.CharField(label='Centre Fees',
                                          widget=forms.NumberInput(
                                              attrs={'class': 'mdl-textfield__input', 'autocomplete': 'on'}))

    class Meta:
        model = Challan
        exclude = ['course_name', 'course']


class RegisterStudentForm(forms.ModelForm):
    registration_id = forms.CharField(label='Registration Id',
                                      widget=forms.TextInput(
                                          attrs={'class': 'mdl-textfield__input', 'autocomplete': 'on'}))
    semester = forms.CharField(label='Semester',
                               widget=forms.NumberInput(attrs={'class': 'mdl-textfield__input', 'autocomplete': 'on'}))

    class Meta:
        model = StudentDetail
        exclude = ['student', 'paid', 'roll']


class StudentCustomUserForm(forms.ModelForm):
    email = forms.CharField(label='Email',
                            widget=forms.EmailInput(attrs={'class': 'mdl-textfield__input', 'autocomplete': 'on'}))

    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'mdl-textfield__input'}))
    username = forms.CharField(label='Username',
                               widget=forms.TextInput(attrs={'class': 'mdl-textfield__input', 'autocomplete': 'on'}))
    first_name = forms.CharField(label='First Name',
                                 widget=forms.TextInput(attrs={'class': 'mdl-textfield__input', 'autocomplete': 'on'}))
    last_name = forms.CharField(label='Last Name',
                                widget=forms.TextInput(attrs={'class': 'mdl-textfield__input', 'autocomplete': 'on'}))

    class Meta:
        model = CustomUser
        exclude = ['is_active', 'is_admin', 'last_login', 'designation']
