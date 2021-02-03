from django.shortcuts import render, redirect
from .models import Student, Teacher, Lesson, Message,LessonStatus
from .forms import SignUpForm , BookLessonForm
from django.contrib.auth import login, authenticate
from datetime import datetime
from django.views.generic import ListView, DetailView
from django.core.exceptions import PermissionDenied

class TeacherListView(ListView):
    model = Teacher
    template_name = 'my_class_app/teachers.html'


class TeacherDetailView(DetailView):
    model = Teacher
    template_name = 'my_class_app/teacher.html'


class StudentDetailView(DetailView):
    model = Student
    template_name = 'my_class_app/student.html'


def index_view(request):
    return render(request, 'my_class_app/index.html')


def message_view(request):
    message = Message.objects.get(id=request.GET['id'])
    message.is_read = True
    message.save()

    referrer = request.GET['r']
    if message.to_user == request.user:
        if referrer == 's':
            sender_name = Teacher.objects.get(user=message.from_user).name
            show_btns=False
        elif referrer == 't':
            sender_name = Student.objects.get(user=message.from_user).name
            show_btns = True
        message.sender_name = sender_name
        return render(request, 'my_class_app/message.html', {'message': message, 'show_btns':show_btns})
    else:
        return render(request, 'my_class_app/message.html', {'message': None})



def reply_view(request):
    message_id = request.POST['id']
    message = Message.objects.get(id=message_id)
    if message.to_user == request.user:
        teacher = Teacher.objects.get(user=request.user)
        lesson = message.lesson
        if '_cancel' in request.POST:
            lesson.status = int(LessonStatus.CANCELLED)
            body = f'Lesson Cancelled!\nBest regards,\n{teacher.name}' + message.body
        elif '_accept' in request.POST:
            lesson.status = int(LessonStatus.ACCEPTED)
            body = f'Lesson Accepted!\nBest regards,\n{teacher.name}' + message.body
        lesson.save()
        message.is_read=True
        message.save()
        title = 'Re: ' + message.title

        reply_message = Message(from_user=message.to_user, to_user=message.from_user, lesson=lesson, is_read=False,
                                title=title, body=body)
        reply_message.save()
        return redirect('/teacher_home/')



def book_view(request):
    date_str = request.POST.get("date", "")
    date = datetime.strptime(date_str, "%m/%d/%Y")
    teacher_id = request.POST.get("teacher_id", "")
    teacher = Teacher.objects.get(id=teacher_id)
    student = Student.objects.get(user=request.user)

    lesson = Lesson(student=student, teacher=teacher, date_time=date)
    lesson.save()
    title = f"Lesson with {student.name} at {date_str}"
    body = f"""
Hi {teacher.name}! 

I'd like to schedule a lesson with you for {date_str}.

Best regards, 

{student.name}

"""

    message = Message(from_user=request.user, to_user=teacher.user, title=title, body=body, is_read=False, lesson=lesson)
    message.save()
    return render(request, 'my_class_app/thanks.html') 


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                print('signup_view authenticate user:', user)
                name = request.POST.get("name","")
                print('name:', name)
                phone = request.POST.get("phone", "")
                print('phone:', phone)
                student = Student(name=name, phone=phone, user=user)
                student.save()
                login(request, user)
                return redirect('student')
            else:
                render(request, 'my_class_app/signup.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'my_class_app/signup.html', {'form': form})


def student_home_view(request):
    try:
        student = Student.objects.get(user=request.user)
    except:
         return redirect('/signin')
    teachers = Teacher.objects.all()
    users_teachers = dict((t.user.id, t) for t in teachers)
    lessons = Lesson.objects.filter(student=student, status=int(LessonStatus.ACCEPTED)).order_by('date_time').reverse()
    messages = Message.objects.filter(to_user=student.user).order_by('id').reverse()
    for message in messages:
        message.sender_name = users_teachers[message.from_user.id].name

    return render(request, 'my_class_app/student_home.html', {'student': student, 'teachers': teachers,
        'lessons':lessons, 'messages': messages, 'form': BookLessonForm()})


def teacher_home_view(request):
    try:
        teacher = Teacher.objects.get(user=request.user)
    except:
         return redirect('/teacher_signin')

    students = Student.objects.all()
    lessons = Lesson.objects.filter(teacher=teacher, status=int(LessonStatus.ACCEPTED)).order_by('date_time').reverse()
    messages = Message.objects.filter(to_user=teacher.user).order_by('id').reverse()
    users_students = dict((t.user.id, t) for t in students)
    for message in messages:
        message.sender_name = users_students[message.from_user.id].name

    return render(request, 'my_class_app/teacher_home.html', {'students': students, 'teacher': teacher,
                                                              'lessons':lessons, 'messages': messages })

