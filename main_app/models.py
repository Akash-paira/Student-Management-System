from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.hashers import make_password


# -------------------------
# Custom User Manager
# -------------------------
class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, password, **extra_fields)


# -------------------------
# Custom User
# -------------------------
class CustomUser(AbstractUser):

    USER_TYPE = (
        ("1", "HOD"),
        ("2", "Staff"),
        ("3", "Student"),
    )

    username = None
    email = models.EmailField(unique=True)

    user_type = models.CharField(max_length=1, choices=USER_TYPE, default="1")
    gender = models.CharField(max_length=10, blank=True)
    profile_pic = models.ImageField(upload_to="profile_pic/", blank=True, null=True)
    address = models.TextField(blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# -------------------------
# Admin
# -------------------------
class Admin(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.admin.email


# -------------------------
# Course
# -------------------------
class Course(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# -------------------------
# Session
# -------------------------
class Session(models.Model):
    start_year = models.DateField()
    end_year = models.DateField()

    def __str__(self):
        return f"{self.start_year} - {self.end_year}"


# -------------------------
# Staff
# -------------------------
class Staff(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.admin.first_name} {self.admin.last_name}"


# -------------------------
# Student
# -------------------------
class Student(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.admin.email
    

#-------------------------
# Subject
#------------------------
class Subject(models.Model):
    name = models.CharField(max_length=100)

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    staff = models.ForeignKey(
        Staff,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Attendance(models.Model):

    session = models.ForeignKey(
        Session,
        on_delete=models.DO_NOTHING
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.DO_NOTHING
    )

    date = models.DateField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.subject.name} - {self.date}"


class AttendanceReport(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.DO_NOTHING
    )

    attendance = models.ForeignKey(
        Attendance,
        on_delete=models.CASCADE
    )

    status = models.BooleanField(default=False)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.student.admin.first_name} - {self.attendance.date}"

#Leave Section

class LeaveReportStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.CharField(max_length=60)
    message = models.TextField()
    status = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LeaveReportStaff(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    date = models.CharField(max_length=60)
    message = models.TextField()
    status = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedbackStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    feedback = models.TextField()
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedbackStaff(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    feedback = models.TextField()
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class NotificationStaff(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)