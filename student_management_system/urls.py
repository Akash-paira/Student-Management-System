from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

from . import views, hod_views, staff_views, student_views

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", views.login_page, name="login"),
    path("doLogin/", views.doLogin, name="do_login"),

    # path("accounts/", include("django.contrib.auth.urls")),

    path("hod/home/", hod_views.admin_home, name="admin_home"),

    path("add_course/", hod_views.add_course, name="add_course"),
    path("save_course/", hod_views.save_course, name="save_course"),
    path("manage_course/", hod_views.manage_course, name="manage_course"),
    path("edit_course/<str:course_id>/", hod_views.edit_course, name="edit_course"),
    path("delete_course/<str:course_id>/", hod_views.delete_course, name="delete_course"),
    path("update_course/<str:course_id>/", hod_views.update_course, name="update_course"),
    path("add_session/", hod_views.add_session, name="add_session"),
    path("save_session/", hod_views.save_session, name="save_session"),
    path("manage_session/", hod_views.manage_session, name="manage_session"),
    path("edit_session/<str:session_id>/", hod_views.edit_session, name="edit_session"),
    path("update_session/<str:session_id>/", hod_views.update_session, name="update_session"),
    path("delete_session/<str:session_id>/", hod_views.delete_session, name="delete_session"),
    path("logout/", views.logout_user, name="user_logout"),
    path("add_staff/", hod_views.add_staff, name="add_staff"),
    path("save_staff/", hod_views.save_staff, name="save_staff"),
    path("manage_staff/", hod_views.manage_staff, name="manage_staff"),
    path(
    "check_email_availability/",
    views.check_email_availability,
    name="check_email_availability",
    ),
    path("edit_staff/<str:staff_id>/", hod_views.edit_staff, name="edit_staff"),
    path("update_staff/<str:staff_id>/", hod_views.update_staff, name="update_staff"),
    path("delete_staff/<str:staff_id>/", hod_views.delete_staff, name="delete_staff"),
    path("add_student/", hod_views.add_student, name="add_student"),
    path("save_student/", hod_views.save_student, name="save_student"),
    path("manage_student/", hod_views.manage_student, name="manage_student"),
    path("edit_student/<str:student_id>/", hod_views.edit_student, name="edit_student"),
    path("update_student/<str:student_id>/", hod_views.update_student, name="update_student"),
    path("delete_student/<str:student_id>/", hod_views.delete_student, name="delete_student"),
    path(
    "add_subject/",
    hod_views.add_subject,
    name="add_subject",
),

    path(
        "save_subject/",
        hod_views.save_subject,
        name="save_subject",
    ),

    path(
    "edit_subject/<str:subject_id>/",
    hod_views.edit_subject,
    name="edit_subject",
),

    path(
            "update_subject/<str:subject_id>/",
            hod_views.update_subject,
            name="update_subject",
        ),

    path(
            "delete_subject/<str:subject_id>/",
            hod_views.delete_subject,
            name="delete_subject",
    ),
    path("manage_subject/", hod_views.manage_subject, name="manage_subject"),
    
    path(
    "admin_view_attendance/",
    hod_views.admin_view_attendance,
    name="admin_view_attendance",
    ),

    path(
    "get_admin_attendance/",
    hod_views.get_admin_attendance,
    name="get_admin_attendance",
    ),
    path(
    "get_attendance/",
    hod_views.get_attendance,
    name="get_attendance",
    ),
    path(
    "staff_leave_view/",
    hod_views.view_staff_leave,
    name="staff_leave_view",
    ),

    path(
        "student_leave_view/",
        hod_views.view_student_leave,
        name="student_leave_view",
    ),

    path(
    "staff_feedback_message/",
    hod_views.staff_feedback_message,
    name="staff_feedback_message",
    ),

    path(
        "student_feedback_message/",
        hod_views.student_feedback_message,
        name="student_feedback_message",
    ),

        # Notification
    path(
        "staff_notification/",
        hod_views.staff_notification,
        name="staff_notification",
    ),

    path(
        "student_notification/",
        hod_views.student_notification,
        name="student_notification",
    ),

    path(
        "send_staff_notification/",
        hod_views.send_staff_notification,
        name="send_staff_notification",
    ),

    path(
        "send_student_notification/",
        hod_views.send_student_notification,
        name="send_student_notification",
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)