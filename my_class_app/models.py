from django.db import models
from django.contrib.auth.models import User
from enum import IntEnum

class Student(models.Model):
    name = models.CharField(max_length=64)
    phone = models.CharField(max_length=64)

    user = models.OneToOneField(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.name
    
    def lesson_count(self):
        result = Lesson.objects.filter(student=self).count()
        return result
    

class Teacher(models.Model):
    name = models.CharField(max_length=64)
    degree = models.CharField(max_length=64)
    rate = models.IntegerField()

    user = models.OneToOneField(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

class LessonStatus(IntEnum):
    NEW = 0
    ACCEPTED = 1
    CANCELLED = 2
    FINISHED = 3


class Lesson(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT)
    #Date
    date_time = models.DateTimeField()
    status = models.IntegerField(default=int(LessonStatus.NEW))


class Message(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='%(class)s_from')
    to_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='%(class)s_to')
    title = models.CharField(max_length=200)
    body = models.CharField(max_length=4000)
    is_read = models.BooleanField()
    lesson = models.ForeignKey(Lesson, on_delete=models.PROTECT, default=None)


