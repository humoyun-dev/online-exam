from django.shortcuts import render, get_object_or_404, redirect
from .models import Exam, Question, Option, Result, Answer
from django.contrib import messages
from .forms import OptionForm

def exam_list(request):
    exams = Exam.objects.all()

    if request.user.is_authenticated:
        if request.user.is_teacher:
            return render(request, 'teacher/exams/exam_list.html')
        elif request.user.is_student:
            return render(request, 'student/exams/exam_list.html')
    
    return render(request, 'staff/exams/exam_list.html', {'exams': exams})

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