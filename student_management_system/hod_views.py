from django.shortcuts import render, redirect
from django.contrib import messages
from main_app.models import Session, Student, Staff, Course,CustomUser
from main_app.forms import CourseForm, StudentForm, SubjectForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from main_app.forms import CourseForm, SessionForm
from django.urls import reverse
from main_app.forms import StaffForm
from django.contrib.auth.hashers import make_password
from main_app.forms import StaffForm
from main_app.models import Subject


def admin_home(request):
    context = {
        "page_title": "HOD Dashboard",
        "total_students": Student.objects.count(),
        "total_staff": Staff.objects.count(),
        "total_course": Course.objects.count(),
        "total_subject": 0,
        "attendance_list": [],
        "subject_list": [],
    }
    return render(request, "hod_template/home_content.html", context)

def add_course(request):

    form = CourseForm()

    context = {
        "page_title": "Add Course",
        "form": form,
        "action_path": "/save_course/",
    }

    return render(
        request,
        "hod_template/add_course_template.html",
        context
    )

def save_course(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect("add_course")

    form = CourseForm(request.POST)

    if form.is_valid():
        form.save()
        messages.success(request, "Course Added Successfully")
    else:
        messages.error(request, "Course Could Not Be Added")

    return redirect("add_course")

def manage_course(request):
    courses = Course.objects.all()

    context = {
        "courses": courses,
        "page_title": "Manage Course"
    }

    return render(request, "hod_template/manage_course_template.html", context)

def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    form = CourseForm(instance=course)

    context = {
        "form": form,
        "page_title": "Edit Course",
        "action_path": f"/update_course/{course_id}/",
    }

    return render(request, "hod_template/edit_course_template.html", context)


def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    try:
        course.delete()
        messages.success(request, "Course Deleted Successfully")
    except Exception:
        messages.error(request, "Failed to Delete Course")

    return redirect("manage_course")

def update_course(request, course_id):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect("manage_course")

    course = get_object_or_404(Course, id=course_id)

    form = CourseForm(request.POST, instance=course)

    if form.is_valid():
        form.save()
        messages.success(request, "Course Updated Successfully")
        return redirect("manage_course")

    messages.error(request, "Course Could Not Be Updated")
    return redirect("edit_course", course_id=course.id)

def add_session(request):
    form = SessionForm()

    context = {
        "form": form,
        "page_title": "Add Session",
        "action_path": reverse("save_session"),
    }

    return render(request, "hod_template/add_session_template.html", context)

def save_session(request):

    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect("add_session")

    form = SessionForm(request.POST)

    if form.is_valid():
        form.save()
        messages.success(request, "Session Added Successfully")
    else:
        messages.error(request, "Failed To Add Session")

    return redirect("add_session")

def manage_session(request):

    sessions = Session.objects.all()

    context = {
        "sessions": sessions,
        "page_title": "Manage Session"
    }

    return render(request,
                  "hod_template/manage_session_template.html",
                  context)

def edit_session(request, session_id):

    session = get_object_or_404(Session, id=session_id)

    form = SessionForm(instance=session)

    context = {
        "form": form,
        "page_title": "Edit Session",
        "action_path": reverse(
            "update_session",
            kwargs={"session_id": session.id}
        )
    }

    return render(
        request,
        "hod_template/edit_session_template.html",
        context
    )
def update_session(request, session_id):

    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect("manage_session")

    session = get_object_or_404(Session, id=session_id)

    form = SessionForm(request.POST, instance=session)

    if form.is_valid():
        form.save()
        messages.success(request, "Session Updated Successfully")
    else:
        messages.error(request, "Failed To Update Session")

    return redirect("manage_session")

def delete_session(request, session_id):

    session = get_object_or_404(Session, id=session_id)

    try:
        session.delete()
        messages.success(request, "Session Deleted Successfully")
    except Exception:
        messages.error(request, "Failed To Delete Session")

    return redirect("manage_session")

def add_staff(request):

    form = StaffForm()

    context = {
        "form": form,
        "page_title": "Add Staff",
        "action_path": reverse("save_staff"),
    }

    return render(
        request,
        "hod_template/add_staff_template.html",
        context,
    )

def save_staff(request):

    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect("add_staff")

    form = StaffForm(request.POST, request.FILES)

    if form.is_valid():

        try:
            user = CustomUser.objects.create(
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                email=form.cleaned_data["email"],
                password=make_password(form.cleaned_data["password"]),
                gender=form.cleaned_data["gender"],
                address=form.cleaned_data["address"],
                profile_pic=form.cleaned_data["profile_pic"],
                user_type="2",
            )

            Staff.objects.create(
                admin=user,
                course=form.cleaned_data["course"],
            )

            messages.success(request, "Staff Added Successfully")

        except Exception as e:
            print(e)
            messages.error(request, "Failed To Add Staff")

    else:
        messages.error(request, "Invalid Form Data")

    return redirect("add_staff")

def manage_staff(request):
    staffs = Staff.objects.select_related("admin", "course").all()

    context = {
        "staffs": staffs,
        "page_title": "Manage Staff"
    }

    return render(request,
                  "hod_template/manage_staff_template.html",
                  context)

def edit_staff(request, staff_id):

    staff = Staff.objects.get(id=staff_id)

    form = StaffForm(initial={
        "first_name": staff.admin.first_name,
        "last_name": staff.admin.last_name,
        "email": staff.admin.email,
        "gender": staff.admin.gender,
        "address": staff.admin.address,
        "course": staff.course,
    })

    context = {
        "form": form,
        "staff_id": staff_id,
        "page_title": "Edit Staff",
        "action_path": f"/update_staff/{staff_id}/",
    }

    return render(
        request,
        "hod_template/edit_staff_template.html",
        context,
    )

def update_staff(request, staff_id):

    if request.method != "POST":
        messages.error(request, "Invalid Request")
        return redirect("manage_staff")

    try:
        staff = Staff.objects.get(id=staff_id)
        admin = staff.admin

        # Basic Details
        admin.first_name = request.POST.get("first_name")
        admin.last_name = request.POST.get("last_name")
        admin.email = request.POST.get("email")
        admin.gender = request.POST.get("gender")
        admin.address = request.POST.get("address")

        # Password (Update only if entered)
        password = request.POST.get("password")
        if password.strip():
            admin.set_password(password)

        # Profile Picture
        if "profile_pic" in request.FILES:
            admin.profile_pic = request.FILES["profile_pic"]

        # Course
        staff.course_id = request.POST.get("course")

        admin.save()
        staff.save()

        messages.success(request, "Staff Updated Successfully")

    except Exception as e:
        print(e)
        messages.error(request, "Failed To Update Staff")

    return redirect("manage_staff")

def delete_staff(request, staff_id):

    try:
        staff = Staff.objects.get(id=staff_id)

        # OneToOne relation hai
        staff.admin.delete()

        messages.success(request, "Staff Deleted Successfully")

    except Exception as e:
        print(e)
        messages.error(request, "Unable to Delete Staff")

    return redirect("manage_staff")


def add_student(request):

    form = StudentForm()

    context = {
        "form": form,
        "page_title": "Add Student",
        "action_path": reverse("save_student"),
    }

    return render(
        request,
        "hod_template/add_student_template.html",
        context,
    )

def save_student(request):

    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect("add_student")

    form = StudentForm(request.POST, request.FILES)

    if form.is_valid():

        try:

            user = CustomUser.objects.create(
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                email=form.cleaned_data["email"],
                password=make_password(form.cleaned_data["password"]),
                gender=form.cleaned_data["gender"],
                address=form.cleaned_data["address"],
                profile_pic=form.cleaned_data["profile_pic"],
                user_type="3",
            )

            Student.objects.create(
                admin=user,
                course=form.cleaned_data["course"],
                session=form.cleaned_data["session"],
            )

            messages.success(request, "Student Added Successfully")

        except Exception as e:
            print(e)
            messages.error(request, "Failed To Add Student")

    else:
        messages.error(request, "Invalid Form Data")

    return redirect("add_student")

def manage_student(request):

    students = Student.objects.select_related(
        "admin",
        "course",
        "session"
    ).all()

    context = {
        "students": students,
        "page_title": "Manage Student",
    }

    return render(
        request,
        "hod_template/manage_student_template.html",
        context,
    )

def edit_student(request, student_id):

    student = get_object_or_404(Student, id=student_id)

    initial_data = {
        "first_name": student.admin.first_name,
        "last_name": student.admin.last_name,
        "email": student.admin.email,
        "gender": student.admin.gender,
        "address": student.admin.address,
        "course": student.course,
        "session": student.session,
    }

    form = StudentForm(initial=initial_data)
    form.fields["password"].required = False

    context = {
        "form": form,
        "student": student,
        "page_title": "Edit Student",
        "action_path": reverse("update_student", kwargs={"student_id": student.id}),
        "button_text": "Update Student",
    }

    return render(
        request,
        "hod_template/edit_student_template.html",
        context,
    )

def update_student(request, student_id):

    if request.method != "POST":
        messages.error(request, "Invalid Request")
        return redirect("manage_student")

    student = get_object_or_404(Student, id=student_id)

    form = StudentForm(request.POST, request.FILES)
    form.fields["password"].required = False

    if form.is_valid():

        try:

            user = student.admin

            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.email = form.cleaned_data["email"]
            user.gender = form.cleaned_data["gender"]
            user.address = form.cleaned_data["address"]

            if form.cleaned_data["password"]:
                user.password = make_password(form.cleaned_data["password"])

            if request.FILES.get("profile_pic"):
                user.profile_pic = request.FILES["profile_pic"]

            user.save()

            student.course = form.cleaned_data["course"]
            student.session = form.cleaned_data["session"]
            student.save()

            messages.success(request, "Student Updated Successfully")

        except Exception as e:
            print(e)
            messages.error(request, "Failed To Update Student")

    else:
        messages.error(request, "Invalid Form Data")

    return redirect("manage_student")

def delete_student(request, student_id):

    student = get_object_or_404(Student, id=student_id)

    try:

        student.admin.delete()

        messages.success(request, "Student Deleted Successfully")

    except Exception as e:

        print(e)

        messages.error(request, "Failed To Delete Student")

    return redirect("manage_student")

def add_subject(request):

    form = SubjectForm()

    context = {
        "form": form,
        "page_title": "Add Subject",
        "action_path": reverse("save_subject"),
    }

    return render(
        request,
        "hod_template/add_subject_template.html",
        context,
    )

def save_subject(request):

    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect("add_subject")

    form = SubjectForm(request.POST)

    if form.is_valid():

        try:

            Subject.objects.create(
                name=form.cleaned_data["subject_name"],
                course=form.cleaned_data["course"],
                staff=form.cleaned_data["staff"],
            )

            messages.success(request, "Subject Added Successfully")

        except Exception as e:
            print(e)
            messages.error(request, "Failed To Add Subject")

    else:
        messages.error(request, "Invalid Form Data")

    return redirect("add_subject")

def manage_subject(request):

    subjects = Subject.objects.select_related(
        "course",
        "staff",
        "staff__admin"
    ).all()

    context = {
        "subjects": subjects,
        "page_title": "Manage Subject",
    }

    return render(
        request,
        "hod_template/manage_subject_template.html",
        context,
    )

def edit_subject(request, subject_id):

    subject = get_object_or_404(Subject, id=subject_id)

    form = SubjectForm(initial={
        "subject_name": subject.name,
        "course": subject.course,
        "staff": subject.staff,
    })

    context = {
        "form": form,
        "page_title": "Edit Subject",
        "action_path": reverse(
            "update_subject",
            kwargs={"subject_id": subject.id}
        ),
        "button_text": "Update Subject",
    }

    return render(
        request,
        "hod_template/edit_subject_template.html",
        context,
    )

def update_subject(request, subject_id):

    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect("manage_subject")

    form = SubjectForm(request.POST)

    if form.is_valid():

        try:

            subject = get_object_or_404(
                Subject,
                id=subject_id
            )

            subject.name = form.cleaned_data["subject_name"]
            subject.course = form.cleaned_data["course"]
            subject.staff = form.cleaned_data["staff"]

            subject.save()

            messages.success(
                request,
                "Subject Updated Successfully"
            )

        except Exception as e:

            print(e)

            messages.error(
                request,
                "Failed To Update Subject"
            )

    else:

        messages.error(
            request,
            "Invalid Form Data"
        )

    return redirect("manage_subject")


def delete_subject(request, subject_id):

    subject = get_object_or_404(
        Subject,
        id=subject_id
    )

    try:

        subject.delete()

        messages.success(
            request,
            "Subject Deleted Successfully"
        )

    except Exception as e:

        print(e)

        messages.error(
            request,
            "Failed To Delete Subject"
        )

    return redirect("manage_subject")