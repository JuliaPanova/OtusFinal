from django.contrib import admin
from .models import Teacher, Student, Lesson, Message

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Lesson)
admin.site.register(Message)
