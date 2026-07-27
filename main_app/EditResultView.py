from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.urls import reverse

from .forms import EditResultForm
from .models import Staff, Student, Subject, StudentResult


class EditResultView(View):

    def get(self, request):
        form = EditResultForm()

        staff = get_object_or_404(
            Staff,
            admin=request.user
        )

        form.fields["subject"].queryset = Subject.objects.filter(
            staff=staff
        )

        context = {
            "page_title": "Edit Student Result",
            "form": form,
        }

        return render(
            request,
            "staff_template/edit_student_result.html",
            context,
        )

    def post(self, request):
        form = EditResultForm(request.POST)

        staff = get_object_or_404(
            Staff,
            admin=request.user
        )

        form.fields["subject"].queryset = Subject.objects.filter(
            staff=staff
        )

        subject_id = request.POST.get("subject")
        session_id = request.POST.get("session")

        if subject_id and session_id:
            subject = get_object_or_404(
                Subject,
                id=subject_id
            )

            form.fields["student"].queryset = Student.objects.filter(
                course=subject.course,
                session_id=session_id
            )

        if form.is_valid():

            student = form.cleaned_data["student"]
            subject = form.cleaned_data["subject"]
            test = form.cleaned_data["test"]
            exam = form.cleaned_data["exam"]

            try:
                result = StudentResult.objects.get(
                    student=student,
                    subject=subject
                )

                result.test = test
                result.exam = exam
                result.save()

                messages.success(
                    request,
                    "Result updated successfully."
                )

                return redirect("edit_student_result")

            except StudentResult.DoesNotExist:
                messages.error(
                    request,
                    "Result not found."
                )

        context = {
            "page_title": "Edit Student Result",
            "form": form,
        }

        return render(
            request,
            "staff_template/edit_student_result.html",
            context,
        )