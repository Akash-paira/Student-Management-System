from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views, hod_views, staff_views, student_views

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", views.login_page, name="login"),
    path("doLogin/", views.doLogin, name="do_login"),

    path("accounts/", include("django.contrib.auth.urls")),
    path("hod/home/", hod_views.admin_home, name="admin_home"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)