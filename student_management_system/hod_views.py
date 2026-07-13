from django.shortcuts import render, redirect
from django.contrib import messages
from main_app.models import Session, Student, Staff, Course
from main_app.forms import CourseForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from main_app.forms import CourseForm, SessionForm
from django.urls import reverse


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