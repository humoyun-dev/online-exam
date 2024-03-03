from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from django.http import HttpResponseNotFound


def custom_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    login_view = LoginView.as_view(
        template_name='registration/login.html',
        extra_context={'next': request.GET.get('next', '/')},
    )
    
    return login_view(request)

@login_required
def home(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return render(request, 'teacher/teacher.html')
        elif request.user.is_student:
            return render(request, 'student/student.html')
    return render(request, 'staff/staff.html')

@login_required
def student_list(request):
    students = CustomUser.objects.filter(is_student=True)
    num_students = students.count()
    
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return render(request, 'teacher/students/students.html', {'students': students , 'num_students': num_students})
        elif request.user.is_student:            
            return HttpResponseNotFound('<h1>Page not found</h1>')

    return render(request, 'staff/students/students.html', {'students': students, 'num_students': num_students})

@login_required
def student_detail_view(request, pk):
    student = get_object_or_404(CustomUser, pk=pk, is_student=True)

    if request.user.is_authenticated:
        if request.user.is_teacher:
            return render(request, 'teacher/students/student_detail.html', {'student': student})
        elif request.user.is_student:
            return HttpResponseNotFound('<h1>Page not found</h1>')

    return render(request, 'staff/students/student_detail.html', {'student': student})

def logout_view(request):
    logout(request)
    return redirect('login')