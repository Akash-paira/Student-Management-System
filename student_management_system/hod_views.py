from django.shortcuts import render
from main_app.models import Student, Staff, Course

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