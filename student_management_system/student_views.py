from django.shortcuts import render, redirect, get_object_or_404
import math
from main_app.models import *
from datetime import datetime
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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
