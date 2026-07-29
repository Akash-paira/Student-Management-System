from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from main_app.EditResultView import *

from . import views, hod_views, staff_views, student_views

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", views.login_page, name="login"),
    path("doLogin/", views.doLogin, name="do_login"),

    # path("accounts/", include("django.contrib.auth.urls")),

    path("hod/home/", hod_views.admin_home, name="admin_home"),

    path("hod/home/add_course/", hod_views.add_course, name="add_course"),
    path("save_course/", hod_views.save_course, name="save_course"),
    path("hod/home/manage_course/", hod_views.manage_course, name="manage_course"),
    path("hod/home/edit_course/<str:course_id>/", hod_views.edit_course, name="edit_course"),
    path("hod/home/delete_course/<str:course_id>/", hod_views.delete_course, name="delete_course"),
    path("hod/home/update_course/<str:course_id>/", hod_views.update_course, name="update_course"),
    path("hod/home/add_session/", hod_views.add_session, name="add_session"),
    path("hod/home/save_session/", hod_views.save_session, name="save_session"),
    path("hod/home/manage_session/", hod_views.manage_session, name="manage_session"),
    path("hod/home/edit_session/<str:session_id>/", hod_views.edit_session, name="edit_session"),
    path("hod/home/update_session/<str:session_id>/", hod_views.update_session, name="update_session"),
    path("delete_session/<str:session_id>/", hod_views.delete_session, name="delete_session"),
    path("logout/", views.logout_user, name="user_logout"),
    path("hod/home/add_staff/", hod_views.add_staff, name="add_staff"),
    path("hod/home/save_staff/", hod_views.save_staff, name="save_staff"),
    path("hod/home/manage_staff/", hod_views.manage_staff, name="manage_staff"),
    path(
    "hod/home/check_email_availability/",
    views.check_email_availability,
    name="check_email_availability",
    ),
    path("hod/home/edit_staff/<str:staff_id>/", hod_views.edit_staff, name="edit_staff"),
    path("hod/home/update_staff/<str:staff_id>/", hod_views.update_staff, name="update_staff"),
    path("hod/home/delete_staff/<str:staff_id>/", hod_views.delete_staff, name="delete_staff"),
    path("hod/home/add_student/", hod_views.add_student, name="add_student"),
    path("hod/home/save_student/", hod_views.save_student, name="save_student"),
    path("hod/home/manage_student/", hod_views.manage_student, name="manage_student"),
    path("hod/home/edit_student/<str:student_id>/", hod_views.edit_student, name="edit_student"),
    path("hod/home/update_student/<str:student_id>/", hod_views.update_student, name="update_student"),
    path("hod/home/delete_student/<str:student_id>/", hod_views.delete_student, name="delete_student"),

    # Subject Management

    path(
    "hod/home/add_subject/",
    hod_views.add_subject,
    name="add_subject",
),

    path(
        "hod/home/save_subject/",
        hod_views.save_subject,
        name="save_subject",
    ),

    path(
    "hod/home/edit_subject/<str:subject_id>/",
    hod_views.edit_subject,
    name="edit_subject",
),

    path(
            "hod/home/update_subject/<str:subject_id>/",
            hod_views.update_subject,
            name="update_subject",
        ),

    path(
            "hod/home/delete_subject/<str:subject_id>/",
            hod_views.delete_subject,
            name="delete_subject",
    ),
    path("hod/home/manage_subject/", hod_views.manage_subject, name="manage_subject"),
    
    # Attendance Management

    path(
    "hod/home/admin_view_attendance/",
    hod_views.admin_view_attendance,
    name="admin_view_attendance",
    ),

    path(
    "hod/home/get_admin_attendance/",
    hod_views.get_admin_attendance,
    name="get_admin_attendance",
    ),
    path(
    "hod/home/get_attendance/",
    hod_views.get_attendance,
    name="get_attendance",
    ),

    # Leave Management

    path(
    "hod/home/staff_leave_view/",
    hod_views.view_staff_leave,
    name="staff_leave_view",
    ),

    path(
        "hod/home/student_leave_view/",
        hod_views.view_student_leave,
        name="student_leave_view",
    ),

    # Feedback Management

    path(
    "hod/home/staff_feedback_message/",
    hod_views.staff_feedback_message,
    name="staff_feedback_message",
    ),

    path(
        "hod/home/student_feedback_message/",
        hod_views.student_feedback_message,
        name="student_feedback_message",
    ),

    # Notification
    path(
        "hod/home/staff_notification/",
        hod_views.staff_notification,
        name="staff_notification",
    ),
    path(
        "hod/home/send_staff_notification/",
        hod_views.send_staff_notification,
        name="send_staff_notification",
    ),
    path(
        "hod/home/student_notification/",
        hod_views.student_notification,
        name="student_notification",
    ),

    path(
        "hod/home/send_student_notification/",
        hod_views.send_student_notification,
        name="send_student_notification",
    ),


    # Staff Panel

    path("staff_home/", staff_views.staff_home, name="staff_home"),

    path(
        "staff/attendance/take/",
        staff_views.staff_take_attendance,
        name="staff_take_attendance",
    ),

    path(
        "staff/get_students/",
        staff_views.get_students,
        name="get_students",
    ),

    path(
        "staff/attendance/save/",
        staff_views.save_attendance,
        name="save_attendance",
    ),

    path(
        "staff/attendance/update/",
        staff_views.staff_update_attendance,
        name="staff_update_attendance",
    ),
    path(
        "staff/attendance/fetch/",
        staff_views.get_attendance,
        name="get_attendance",
    ),
    path(
        "staff/attendance/get/",
        staff_views.get_student_attendance,
        name="get_student_attendance",
    ),

    path(
        "staff/attendance/update/save/",
        staff_views.update_attendance,
        name="update_attendance",
    ),

    path(
        "staff/leave/apply/",
        staff_views.staff_apply_leave,
        name="staff_apply_leave",
    ),
    path(
        "staff/leave/save/",
        staff_views.staff_apply_leave_save,
        name="staff_apply_leave_save",
    ),
    

    path(
        "staff/feedback/",
        staff_views.staff_feedback,
        name="staff_feedback",
    ),
    path(
        "staff/feedback/save/",
        staff_views.staff_feedback_save,
        name="staff_feedback_save",
    ),
   
    path(
        "staff/view/notification/",
        staff_views.staff_view_notification,
        name="staff_view_notification",
    ),

    path(
        "staff/student/fetch/",
        staff_views.get_students,
        name="get_students",
    ),
    path(
        "staff/result/add/",
        staff_views.staff_add_result,
        name="staff_add_result",
    ),
    path(
        "staff/result/edit/",
        EditResultView.as_view(),
        name="edit_student_result",
    ),
    path(
        "staff/result/fetch/",
        staff_views.fetch_student_result,
        name="fetch_student_result",
    ),
    path(
        "staff/view/profile/",
        staff_views.staff_view_profile,
        name="staff_view_profile",
    ),

    #------------------------------
    # Student Panel
    #------------------------------

    path("student_home/", student_views.student_home, name="student_home"),

    path(
        "student_view_attendance/",
        student_views.student_view_attendance,
        name="student_view_attendance",
    ),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)