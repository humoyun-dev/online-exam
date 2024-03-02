from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required

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