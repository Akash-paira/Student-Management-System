from django.shortcuts import render, redirect, get_object_or_404
import math
from main_app.models import *
from datetime import datetime
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.urls import reverse
from main_app.forms import *

def student_home(request):
    student = get_object_or_404(
        Student,
        admin=request.user
    )

    subjects = Subject.objects.filter(course=student.course)

    total_subject = subjects.count()

    total_attendance = AttendanceReport.objects.filter(
        student=student
    ).count()

    total_present = AttendanceReport.objects.filter(
        student=student,
        status=True
    ).count()

    if total_attendance == 0:
        percent_present = 0
        percent_absent = 0
    else:
        percent_present = math.floor(
            (total_present / total_attendance) * 100
        )
        percent_absent = 100 - percent_present

    subject_name = []
    data_present = []
    data_absent = []

    for subject in subjects:

        attendance = Attendance.objects.filter(
            subject=subject
        )

        present_count = AttendanceReport.objects.filter(
            attendance__in=attendance,
            student=student,
            status=True
        ).count()

        absent_count = AttendanceReport.objects.filter(
            attendance__in=attendance,
            student=student,
            status=False
        ).count()

        subject_name.append(subject.name)
        data_present.append(present_count)
        data_absent.append(absent_count)

    context = {
        "page_title": "Student Dashboard",
        "total_subject": total_subject,
        "total_attendance": total_attendance,
        "percent_present": percent_present,
        "percent_absent": percent_absent,
        "subjects": subjects,
        "data_name": subject_name,
        "data_present": data_present,
        "data_absent": data_absent,
    }

    return render(
        request,
        "student_template/home_content.html",
        context,
    )

@csrf_exempt
def student_view_attendance(request):
    student = get_object_or_404(
        Student,
        admin=request.user
    )

    # Page Load
    if request.method != "POST":

        subjects = Subject.objects.filter(
            course=student.course
        )

        context = {
            "page_title": "View Attendance",
            "subjects": subjects,
        }

        return render(
            request,
            "student_template/student_view_attendance.html",
            context,
        )

    # AJAX Request
    subject_id = request.POST.get("subject")
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")

    try:
        subject = get_object_or_404(
            Subject,
            id=subject_id,
        )

        start_date = datetime.strptime(
            start_date,
            "%Y-%m-%d",
        )

        end_date = datetime.strptime(
            end_date,
            "%Y-%m-%d",
        )

        attendance = Attendance.objects.filter(
            subject=subject,
            date__range=(start_date, end_date),
        )

        attendance_reports = AttendanceReport.objects.filter(
            attendance__in=attendance,
            student=student,
        )

        attendance_data = []

        for report in attendance_reports:

            attendance_data.append({
                "date": str(report.attendance.date),
                "status": report.status,
            })

        return JsonResponse(
            json.dumps(attendance_data),
            safe=False,
        )

    except Exception as e:
        return JsonResponse(
            {
                "status": False,
                "message": str(e),
            },
            status=400,
        )

def student_view_result(request):
    student = get_object_or_404(
        Student,
        admin=request.user
    )

    results = StudentResult.objects.filter(
        student=student
    ).select_related("subject")

    context = {
        "page_title": "View Results",
        "results": results,
    }

    return render(
        request,
        "student_template/student_view_result.html",
        context,
    )

def student_apply_leave(request):
    student = get_object_or_404(Student, admin=request.user)

    form = StudentLeaveForm()

    context = {
        "page_title": "Apply For Leave",
        "form": form,
        "leave_history": LeaveReportStudent.objects.filter(
            student=student
        ).order_by("-created_at"),
    }

    return render(
        request,
        "student_template/student_apply_leave.html",
        context,
    )

def student_apply_leave_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Request")
        return redirect("student_apply_leave")

    form = StudentLeaveForm(request.POST)

    if form.is_valid():
        student = get_object_or_404(
            Student,
            admin=request.user
        )

        leave = LeaveReportStudent(
            student=student,
            date=form.cleaned_data["leave_date"],
            message=form.cleaned_data["message"],
            status=0
        )

        leave.save()

        messages.success(request, "Leave applied successfully.")

    else:
        messages.error(request, "Please fill all fields correctly.")

    return redirect("student_apply_leave")

def student_feedback(request):
    student = get_object_or_404(
        Student,
        admin=request.user
    )

    form = FeedbackStudentForm()

    context = {
        "page_title": "Student Feedback",
        "form": form,
        "feedbacks": FeedbackStudent.objects.filter(
            student=student
        ).order_by("-created_at"),
    }

    return render(
        request,
        "student_template/student_feedback.html",
        context,
    )

def student_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect("student_feedback")

    form = FeedbackStudentForm(request.POST)

    if form.is_valid():
        feedback = form.cleaned_data["feedback"]

        try:
            student = Student.objects.get(admin=request.user)

            FeedbackStudent.objects.create(
                student=student,
                feedback=feedback,
                reply=""
            )

            messages.success(
                request,
                "Feedback submitted successfully."
            )

        except Exception:
            messages.error(
                request,
                "Could not submit feedback."
            )

    else:
        messages.error(
            request,
            "Form is invalid."
        )

    return redirect("student_feedback")

def student_view_profile(request):
    student = get_object_or_404(
        Student,
        admin=request.user
    )

    if request.method == "POST":
        form = StudentEditForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            admin = student.admin

            admin.first_name = form.cleaned_data["first_name"]
            admin.last_name = form.cleaned_data["last_name"]
            admin.gender = form.cleaned_data["gender"]
            admin.address = form.cleaned_data["address"]

            password = form.cleaned_data.get("password")
            if password:
                admin.set_password(password)

            profile_pic = request.FILES.get("profile_pic")
            if profile_pic:
                admin.profile_pic = profile_pic

            admin.save()
            student.save()

            messages.success(
                request,
                "Profile Updated Successfully."
            )

            if password:
                return redirect("login")

            return redirect("student_view_profile")

        messages.error(
            request,
            "Please correct the errors below."
        )

    else:
        form = StudentEditForm(initial={
            "first_name": student.admin.first_name,
            "last_name": student.admin.last_name,
            "gender": student.admin.gender,
            "address": student.admin.address,
        })

    context = {
        "page_title": "View/Edit Profile",
        "form": form,
    }

    return render(
        request,
        "student_template/student_view_profile.html",
        context,
    )

def student_view_notification(request):
    student = get_object_or_404(
        Student,
        admin=request.user
    )

    notifications = NotificationStudent.objects.filter(
        student=student
    ).order_by("-created_at")

    context = {
        "page_title": "View Notifications",
        "notifications": notifications,
    }

    return render(
        request,
        "student_template/student_view_notification.html",
        context,
    )