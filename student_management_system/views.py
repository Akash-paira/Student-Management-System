from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth import logout
from django.shortcuts import redirect

def login_page(request):
    return render(request, "main_app/login.html")

def admin_home(request):
    return HttpResponse("<h1>Welcome HOD Dashboard</h1>")


def doLogin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)

            if user.user_type == "1":
                return redirect("admin_home")

            elif user.user_type == "2":
                return redirect("staff_home")

            elif user.user_type == "3":
                return redirect("student_home")

        return redirect("login")

    return redirect("login")

def logout_user(request):
    logout(request)
    return redirect("login")