from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import * 


class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = (
        "email",
        "first_name",
        "last_name",
        "user_type",
        "is_staff",
    )

    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {
            "fields": (
                "first_name",
                "last_name",
                "gender",
                "address",
                "profile_pic",
                "user_type",
            )
        }),
        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        ("Important dates", {
            "fields": ("last_login",)
        }),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "user_type",
                ),
            },
        ),
    )

    search_fields = ("email",)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Admin)
admin.site.register(Course)
admin.site.register(Session)
admin.site.register(Subject)
admin.site.register(Staff)
admin.site.register(Attendance)
admin.site.register(AttendanceReport)
admin.site.register(Student)
