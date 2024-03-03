from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Exam, Question, Option, Result, Answer, Course
from .forms import ExamForm , OptionForm
from django.http import HttpResponseNotFound

@login_required
def exam_list(request):
    exams = Exam.objects.all()
    exam_count = exams.count()
    courses = Course.objects.all()
    courses_count = courses.count()

    if request.user.is_authenticated:
        if request.user.is_teacher:
            return render(request, 'teacher/exams/exam_list.html', {'exams': exams, 'exam_count': exam_count})
        elif request.user.is_student:
            return render(request, 'student/exams/course_detail_exam_list.html', {'exams': exams, 'exam_count': exam_count})
        elif request.user.is_staff:
            return render(request, 'staff/exams/course_list.html', {'courses': courses, 'courses_count': courses_count})



def show_exams_staff(request, course_id):
    if request.user.is_authenticated and request.user.is_staff:
        course = get_object_or_404(Course, id=course_id)
        exams = Exam.objects.filter(course=course)
        exam_count = exams.count()
        return render(request, 'staff/exams/course_detail_exam_list.html', {"course": course, 'exams': exams, 'exam_count': exam_count})


def take_exam(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    questions = exam.question_set.all()
    
    if request.method == 'POST':
        form = OptionForm(request.POST, questions=questions)
        if form.is_valid():
            total_mark = 0
            for question in questions:
                selected_option_id = form.cleaned_data.get(f'question_{question.id}')
                if selected_option_id:
                    selected_option = get_object_or_404(Option, pk=selected_option_id)
                    total_mark += question.mark if selected_option.is_correct else 0
            
            # Create a result object for the student's performance in the exam
            result = Result.objects.create(student=request.user, exam=exam, score=total_mark)
            
            # Save the selected options and answers
            for question in questions:
                selected_option_id = form.cleaned_data.get(f'question_{question.id}')
                if selected_option_id:
                    selected_option = get_object_or_404(Option, pk=selected_option_id)
                    is_correct = selected_option.is_correct
                else:
                    is_correct = False
                
                Answer.objects.create(result=result, student=request.user, question=question,
                                       selected_option=selected_option, is_correct=is_correct)
            
            messages.success(request, 'Exam submitted successfully!')
            return redirect('show_result', exam_id=exam_id)
    else:
        form = OptionForm(questions=questions)
        
    return render(request, 'take_exam.html', {'exam': exam, 'questions': questions, 'form': form})

def show_result(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    
    # Get the most recent result for the current student and exam
    result = Result.objects.filter(student=request.user, exam=exam).latest('date_taken')
    
    student_answers = Answer.objects.filter(result=result)
    return render(request, 'show_result.html', {'exam': exam, 'result': result, 'student_answers': student_answers})

@login_required
def add_exam(request):
    if request.user.is_authenticated and request.user.is_teacher:
        if request.method == 'POST':
            form = ExamForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('exam_list')
        else:
            form = ExamForm()
        
        return render(request, 'teacher/exams/add_exam.html', {'form': form})
    elif request.user.is_authenticated and request.user.is_student:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    
    else:
        return render(request, 'staff/exams/add_exam.html', {'form': form})

@login_required
def exam_detail(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    questions = exam.question_set.all() 

    questions_count = questions.count()
    return render(request, 'teacher/exams/exam_detail.html', {'exam': exam , 'questions': questions, 'questions_count': questions_count})