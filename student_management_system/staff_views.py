from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, request
import json
from django.contrib import messages
from django.urls import reverse
# from requests import session
from main_app.models import *
from main_app.EmailBackend import EmailBackend
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from main_app.forms import *



def staff_home(request):
    staff = get_object_or_404(Staff, admin=request.user)

    subjects = Subject.objects.filter(staff=staff)

    total_students = Student.objects.filter(course=staff.course).count()
    total_leave = LeaveReportStaff.objects.filter(staff=staff).count()
    total_subject = subjects.count()
    total_attendance = Attendance.objects.filter(subject__in=subjects).count()

    subject_list = []
    attendance_list = []

    for subject in subjects:
        subject_list.append(subject.name)
        attendance_list.append(
            Attendance.objects.filter(subject=subject).count()
        )

    context = {
        "page_title": f"Staff Panel - {staff.admin.get_full_name()} ({staff.course})",
        "total_students": total_students,
        "total_attendance": total_attendance,
        "total_leave": total_leave,
        "total_subject": total_subject,
        "subject_list": subject_list,
        "attendance_list": attendance_list,
    }

    return render(request, "staff_template/home_content.html", context)


def staff_take_attendance(request):
    """
    Display Take Attendance page for logged-in staff.
    """
    staff = get_object_or_404(
        Staff,
        admin=request.user
    )

    subjects = Subject.objects.filter(
        staff=staff
    ).order_by("name")

    sessions = Session.objects.all()

    context = {
        "page_title": "Take Attendance",
        "subjects": subjects,
        "sessions": sessions,
        "staff": staff,
    }

    return render(
        request,
        "staff_template/staff_take_attendance.html",
        context,
    )

def get_students(request):
    if request.method != "POST":
        return JsonResponse(
            {
                "status": False,
                "message": "Invalid Request"
            },
            status=400
        )

    subject_id = request.POST.get("subject")
    session_id = request.POST.get("session")

    try:
        subject = get_object_or_404(
            Subject,
            id=subject_id
        )

        session = get_object_or_404(
            Session,
            id=session_id
        )

        students = Student.objects.filter(
            course=subject.course,
            session=session
        )

        student_list = []

        for student in students:
            student_list.append(
                {
                    "id": student.id,
                    "name": f"{student.admin.first_name} {student.admin.last_name}"
                }
            )

        return JsonResponse(student_list, safe=False)

    except Exception as e:
        return JsonResponse(
            {
                "status": False,
                "message": str(e)
            },
            status=500
        )


def save_attendance(request):
    if request.method != "POST":
        return JsonResponse(
            {
                "status": False,
                "message": "Invalid Request"
            },
            status=400
        )

    try:
        student_data = request.POST.get("student_ids")
        attendance_date = request.POST.get("date")
        subject_id = request.POST.get("subject")
        session_id = request.POST.get("session")

        students = json.loads(student_data)

        subject = get_object_or_404(
            Subject,
            id=subject_id
        )

        session = get_object_or_404(
            Session,
            id=session_id
        )

        attendance, created = Attendance.objects.get_or_create(
            subject=subject,
            session=session,
            date=attendance_date
        )

        for student in students:

            student_obj = get_object_or_404(
                Student,
                id=student["id"]
            )

            AttendanceReport.objects.update_or_create(
                attendance=attendance,
                student=student_obj,
                defaults={
                    "status": student["status"]
                }
            )

        return HttpResponse("OK")

    except Exception as e:
        return JsonResponse(
            {
                "status": False,
                "message": str(e)
            },
            status=500
        )

def staff_update_attendance(request):
    staff = get_object_or_404(
        Staff,
        admin=request.user
    )

    subjects = Subject.objects.filter(
        staff=staff
    ).order_by("name")

    sessions = Session.objects.all()

    context = {
        "page_title": "Update Attendance",
        "subjects": subjects,
        "sessions": sessions,
    }

    return render(
        request,
        "staff_template/staff_update_attendance.html",
        context
    )

def get_attendance(request):
    if request.method != "POST":
        return JsonResponse([], safe=False)

    subject_id = request.POST.get("subject")
    session_id = request.POST.get("session")

    subject = get_object_or_404(Subject, id=subject_id)
    session = get_object_or_404(Session, id=session_id)

    attendance = Attendance.objects.filter(
        subject=subject,
        session=session
    ).order_by("-date")

    data = []

    for att in attendance:
        data.append({
            "id": att.id,
            "attendance_date": str(att.date)
        })

    return JsonResponse(data, safe=False)


def get_student_attendance(request):
    if request.method != "POST":
        return JsonResponse([], safe=False)

    attendance_id = request.POST.get("attendance_date_id")

    attendance = get_object_or_404(
        Attendance,
        id=attendance_id
    )

    reports = AttendanceReport.objects.filter(
        attendance=attendance
    ).select_related("student__admin")

    data = []

    for report in reports:
        data.append({
            "id": report.student.id,
            "name": f"{report.student.admin.first_name} {report.student.admin.last_name}",
            "status": report.status,
        })

    attendance_id = request.POST.get("attendance_date_id")

    return JsonResponse(data, safe=False)

def update_attendance(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method")

    try:
        attendance_id = request.POST.get("date")
        student_data = json.loads(request.POST.get("student_ids"))

        attendance = Attendance.objects.get(id=attendance_id)

        for student in student_data:
            report = AttendanceReport.objects.get(
                attendance=attendance,
                student_id=student["id"]
            )

            report.status = student["status"]
            report.save()

        return HttpResponse("OK")

    except Exception as e:
        print(e)
        return HttpResponse("ERR")


def staff_apply_leave(request):
    staff = get_object_or_404(
        Staff,
        admin=request.user
    )

    form = StaffLeaveForm()

    leave_history = LeaveReportStaff.objects.filter(
        staff=staff
    ).order_by("-created_at")

    context = {
        "form": form,
        "leave_history": leave_history,
        "action_path": reverse("staff_apply_leave_save"),
        "page_title": "Apply for Leave",
    }

    return render(
        request,
        "staff_template/staff_apply_leave.html",
        context,
    )


def staff_apply_leave_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Request")
        return redirect("staff_apply_leave")

    form = StaffLeaveForm(request.POST)

    if form.is_valid():
        staff = get_object_or_404(
            Staff,
            admin=request.user
        )

        leave = LeaveReportStaff(
            staff=staff,
            date=form.cleaned_data["leave_date"],
            message=form.cleaned_data["message"],
            status=0
        )

        leave.save()

        messages.success(request, "Leave applied successfully.")

    else:
        messages.error(request, "Please fill all fields correctly.")

    return redirect("staff_apply_leave")

def staff_feedback(request):
    staff = get_object_or_404(
        Staff,
        admin=request.user
    )

    form = StaffFeedbackForm()

    feedback_data = FeedbackStaff.objects.filter(
        staff=staff
    ).order_by("-created_at")

    context = {
        "page_title": "Staff Feedback",
        "form": form,
        "feedback_data": feedback_data,
        "action_path": reverse("staff_feedback_save"),
    }

    return render(
        request,
        "staff_template/staff_feedback.html",
        context,
    )
def staff_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Request")
        return redirect("staff_feedback")

    form = StaffFeedbackForm(request.POST)

    if form.is_valid():
        staff = get_object_or_404(
            Staff,
            admin=request.user
        )

        feedback = FeedbackStaff(
            staff=staff,
            feedback=form.cleaned_data["feedback"],
            reply=""
        )

        feedback.save()

        messages.success(request, "Feedback submitted successfully.")

    else:
        messages.error(request, "Please fill all fields correctly.")

    return redirect("staff_feedback")

def staff_view_notification(request):
    staff = get_object_or_404(
        Staff,
        admin=request.user
    )

    notifications = NotificationStaff.objects.filter(
        staff=staff
    ).order_by("-created_at")

    context = {
        "page_title": "View Notifications",
        "notifications": notifications,
    }

    return render(
        request,
        "staff_template/staff_view_notification.html",
        context,
    )

def staff_add_result(request):
    staff = get_object_or_404(
        Staff,
        admin=request.user
    )

    subjects = Subject.objects.filter(
        staff=staff
    )

    sessions = Session.objects.all()

    context = {
        "page_title": "Result Upload",
        "subjects": subjects,
        "sessions": sessions,
    }

    if request.method == "POST":
        try:
            student_id = request.POST.get("student_list")
            subject_id = request.POST.get("subject")
            test = request.POST.get("test")
            exam = request.POST.get("exam")

            student = get_object_or_404(
                Student,
                id=student_id
            )

            subject = get_object_or_404(
                Subject,
                id=subject_id
            )

            result, created = StudentResult.objects.get_or_create(
                student=student,
                subject=subject,
                defaults={
                    "test": test,
                    "exam": exam,
                }
            )

            if not created:
                result.test = test
                result.exam = exam
                result.save()
                messages.success(request, "Result updated successfully.")
            else:
                messages.success(request, "Result saved successfully.")

        except Exception as e:
            messages.error(request, f"Error: {e}")

    return render(
        request,
        "staff_template/staff_add_result.html",
        context,
    )

import json
from django.http import HttpResponse


def fetch_student_result(request):
    if request.method != "POST":
        return HttpResponse("False")

    try:
        subject_id = request.POST.get("subject")
        student_id = request.POST.get("student")

        student = get_object_or_404(
            Student,
            id=student_id
        )

        subject = get_object_or_404(
            Subject,
            id=subject_id
        )

        result = StudentResult.objects.get(
            student=student,
            subject=subject
        )

        data = {
            "test": result.test,
            "exam": result.exam,
        }

        return HttpResponse(json.dumps(data))

    except StudentResult.DoesNotExist:
        return HttpResponse("False")

    except Exception:
        return HttpResponse("False")