from django import forms
from django.contrib import messages
from django.shortcuts import redirect
from .models import Course
from .models import Session, Subject, Student
from .models import Staff, Course, CustomUser

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["name"]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter Course Name"
            })
        }


class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ["start_year", "end_year"]
        widgets = {
            "start_year": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),
            "end_year": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),
        }

class StaffForm(forms.Form):

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )

    password = forms.CharField(
    required=False,
    widget=forms.PasswordInput(attrs={"class": "form-control"})
)

    gender = forms.ChoiceField(
        choices=[
            ("Male", "Male"),
            ("Female", "Female"),
            ("Others", "Others")
        ],
        widget=forms.Select(attrs={"class": "form-control"})
    )

    address = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control"})
    )

    profile_pic = forms.ImageField(required=False)

    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"})
    )

class StudentForm(forms.Form):

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    gender = forms.ChoiceField(
        choices=[
            ("Male", "Male"),
            ("Female", "Female"),
            ("Others", "Others")
        ],
        widget=forms.Select(attrs={"class": "form-control"})
    )

    address = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control"})
    )

    profile_pic = forms.ImageField(required=False)

    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"})
    )

    session = forms.ModelChoiceField(
        queryset=Session.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"})
    )

class SubjectForm(forms.Form):

    subject_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        )
    )

    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-control"}
        )
    )

    staff = forms.ModelChoiceField(
        queryset=Staff.objects.all(),
        widget=forms.Select(
            attrs={"class": "form-control"}
        )
    )


class StaffLeaveForm(forms.Form):
    leave_date = forms.CharField(
        widget=forms.DateInput(attrs={
            "type": "date",
            "class": "form-control"
        })
    )

    message = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 5,
            "placeholder": "Enter your reason for leave"
        })
    )
    
def staff_apply_leave_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect("staff_apply_leave")

    messages.success(request, "Temporary Save Function Working!")
    return redirect("staff_apply_leave")


class StaffFeedbackForm(forms.Form):
    feedback = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Enter your feedback"
            }
        )
    )

class EditResultForm(forms.Form):
    session = forms.ModelChoiceField(
        queryset=Session.objects.all(),
        widget=forms.Select(attrs={
            "class": "form-control"
        })
    )

    subject = forms.ModelChoiceField(
        queryset=Subject.objects.none(),
        widget=forms.Select(attrs={
            "class": "form-control"
        })
    )

    student = forms.ModelChoiceField(
        queryset=Student.objects.none(),
        widget=forms.Select(attrs={
            "class": "form-control"
        })
    )

    test = forms.FloatField(
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "min": 0,
            "max": 40
        })
    )

    exam = forms.FloatField(
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "min": 0,
            "max": 60
        })
    )

class StaffEditForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    gender = forms.ChoiceField(
        choices=[
            ("Male", "Male"),
            ("Female", "Female"),
        ],
        widget=forms.Select(attrs={"class": "form-control"})
    )

    address = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 3,
            }
        )
    )

    profile_pic = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={"class": "form-control"})
    )

    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Leave blank to keep current password",
            }
        )
    )

class StudentLeaveForm(forms.Form):
    leave_date = forms.CharField(
        widget=forms.DateInput(attrs={
            "type": "date",
            "class": "form-control"
        })
    )

    message = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 5,
            "placeholder": "Enter your reason for leave"
        })
    )

def student_apply_leave_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect("student_apply_leave")

    messages.success(request, "Temporary Save Function Working!")
    return redirect("student_apply_leave")
