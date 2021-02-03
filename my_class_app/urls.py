from django.contrib import admin
from django.urls import path, include
from .views import index_view, student_view

app_name = 'my_class_app'

urlpatterns = [
    path('', index_view, name='index'),

]
