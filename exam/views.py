from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.http import HttpResponseNotFound
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count
from .models import *
from .forms import *

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
            return render(request, 'student/exams/exam_list.html', {'exams': exams, 'exam_count': exam_count})
        elif request.user.is_staff:
            return render(request, 'staff/exams/course_list.html', {'courses': courses, 'courses_count': courses_count})

@login_required
def take_exam(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    questions = exam.question_set.all()
    current_time = timezone.now()

    # Check if end_time is None, set it if necessary
    if exam.end_time is None:
        exam.end_time = current_time + timezone.timedelta(minutes=exam.duration_minutes)
        exam.save()

    time_remaining = (exam.end_time - current_time).total_seconds()  # Calculate time remaining in seconds

    if request.method == 'POST':
        form = OptionForm(request.POST, questions=questions)
        if form.is_valid():
            # Your existing code for processing the exam submission
            total_mark = 0
            for question in questions:
                selected_option_id = form.cleaned_data.get(f'question_{question.id}')
                if selected_option_id:
                    selected_option = get_object_or_404(Option, pk=selected_option_id)
                    total_mark += question.mark if selected_option.is_correct else 0
            
            result = Result.objects.create(student=request.user, exam=exam, score=total_mark)
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
    
    return render(request, 'student/exams/take_exam.html', {
        'exam': exam,
        'questions': questions,
        'form': form,
        'time_remaining': time_remaining  # Pass time remaining to the template
    })

@login_required
def show_result(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    result = Result.objects.filter(student=request.user, exam=exam).latest('date_taken')
    
    student_answers = Answer.objects.filter(result=result)
    return render(request, 'student/exams/show_result.html', {'exam': exam, 'result': result, 'student_answers': student_answers})

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

@login_required
def add_question(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        option_formset = OptionFormSet(request.POST)
        if question_form.is_valid() and option_formset.is_valid():
            question = question_form.save(commit=False)
            question.exam = exam
            question.save()
            option_formset.instance = question
            option_formset.save()
            return redirect('exam_detail', exam_id=exam_id)  # Redirect back to the exam detail page
    else:
        question_form = QuestionForm()
        option_formset = OptionFormSet()

    return render(request, 'teacher/exams/add_question.html', {'exam': exam, 'question_form': question_form, 'option_formset': option_formset})

@login_required
def question_detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    exam = get_object_or_404(Exam, pk=question.exam.id)

    return render(request, 'teacher/exams/question_detail.html', {'question': question, 'exam': exam})

@login_required
def edit_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    OptionFormSet = modelformset_factory(Option, fields=('option_text', 'is_correct'), extra=1)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        formset = OptionFormSet(request.POST, queryset=Option.objects.filter(question=question))
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('question_detail', question_id=question_id)
    else:
        form = QuestionForm(instance=question)
        formset = OptionFormSet(queryset=Option.objects.filter(question=question))
    
    return render(request, 'teacher/exams/edit_question.html', {'form': form, 'formset': formset, 'question': question})

@login_required
def delete_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.delete()
    return redirect('exam_detail', exam_id=question.exam.id)

@login_required
def delete_exam(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    
    exam.delete()
    return redirect('exam_list')

@login_required
def student_results(request):
    # Retrieve all results for the current student
    student_results = Result.objects.filter(student=request.user).order_by('-date_taken')
    
    return render(request, 'student/exams/results.html', {'result': student_results})

@login_required
def result_detail(request, result_id):
    result = get_object_or_404(Result, student=request.user, pk=result_id)
    student_answers = Answer.objects.filter(result=result)
    return render(request, 'student/exams/result_detail.html', {'result': result, 'student_answers': student_answers})

@login_required
def show_courses(request):
    courses = Course.objects.annotate(
        exam_count=Count('exam', distinct=True),
        question_count=Count('exam__question', distinct=True)
    )

    if request.user.is_authenticated:
        if request.user.is_teacher:
            return render(request, 'teacher/courses/course_list.html', {'courses': courses})
        elif request.user.is_student:
            return render(request, 'student/courses/course_list.html', {'courses': courses})
        elif request.user.is_staff:
            return render(request, 'staff/courses/course_list.html', {'courses': courses})