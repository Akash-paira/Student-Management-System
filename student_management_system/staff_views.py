from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, request
import json
from django.contrib import messages
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
    print(request.user)
    print(request.user.email)
    print(request.user.id)
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

        print("========== DEBUG ==========")
        print("Subject :", subject.name)
        print("Course  :", subject.course)
        print("Session :", session)

        students = Student.objects.filter(
            course=subject.course,
            session=session
        )

        print("Students Count :", students.count())

        for student in students:
            print(student.admin.first_name, student.admin.last_name)

        print("===========================")

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