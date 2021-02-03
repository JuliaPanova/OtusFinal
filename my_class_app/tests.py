from django.test import TestCase
from .models import Student, Teacher, Lesson
from django.contrib.auth.models import User
from datetime import datetime
from django.test import Client

class TestStudent(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='peter', email='peter@mmmail.com', password='nopass')
        self.user2 = User.objects.create_user(username='kate', email='kate@mmmail.com', password='nopass')
        self.student = Student.objects.create(name='Pete', user=self.user1)
        self.teacher = Teacher.objects.create(name='Kate', user=self.user2, rate=10, degree='Master')
        self.lesson1 = Lesson.objects.create(student=self.student, teacher=self.teacher, date_time=datetime(2021, 2, 4, 20, 0,0))
        self.lesson2 = Lesson.objects.create(student=self.student, teacher=self.teacher, date_time=datetime(2021, 2, 4, 21, 0,0))


    def tearDown(self):
        pass

    def test_str(self):
        self.assertEqual(str(self.student), 'Pete')

    def test_lesson_count(self):
        self.assertEqual(self.student.lesson_count(), 2)
        
class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='peter', email='peter@mmmail.com', password='nopass')
        self.admin1 = User.objects.create_superuser(username='admin', email='admin@mmmail.com', password='admin123456')

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
    def test_teacher(self):
        response = self.client.get('/teachers/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('object_list' in response.context)

    def test_admin_permissions(self):
        self.client.login(username='peter', password='nopass')
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)
        self.client.login(username='admin', password='admin123456')
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)
