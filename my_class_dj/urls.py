from django.contrib import admin
from django.urls import path
from my_class_app.views import index_view, student_home_view, book_view, signup_view, \
    TeacherListView, TeacherDetailView, teacher_home_view, StudentDetailView, message_view, reply_view
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view),
    path('student_home/', student_home_view, name='student'),
    path('student/<int:pk>/', StudentDetailView.as_view()),
    path('book/', book_view, name='book'),
    path('signup/', signup_view),
    path('signin/', auth_views.LoginView.as_view(template_name='my_class_app/signin.html')),
    path('teacher_signin/', auth_views.LoginView.as_view(template_name='my_class_app/teacher_signin.html')),
    path('teacher_home/', teacher_home_view),

    path('teachers/', TeacherListView.as_view()),
    path('teacher/<int:pk>/', TeacherDetailView.as_view()),
    path('message/', message_view, name='message'),
    path('reply/', reply_view, name='message'),

]
