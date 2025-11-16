from django.contrib import admin
from .models import Course, Lesson


@admin.register(Course)
class CoursesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'preview', 'created_at', 'author')
    list_filter = ('id', 'name', 'description', 'preview', 'created_at', 'author')
    search_fields = ('id', 'name', 'description', 'preview', 'created_at', 'author',)


@admin.register(Lesson)
class LessonsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'preview', 'created_at', 'video_url', 'author')
    list_filter = ('id', 'name', 'description', 'preview', 'created_at', 'video_url', 'author')
    search_fields = ('id', 'name', 'description', 'preview', 'created_at', 'video_url', 'author',)
