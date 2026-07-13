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
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)