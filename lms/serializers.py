from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class LessonsByCourseSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['name', 'description', 'preview', 'video_url', ]


class CourseSerializer(ModelSerializer):
    lessons_count = SerializerMethodField()
    lessons = LessonsByCourseSerializer(many=True, read_only=True)

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = [
            'id',
            'name',
            'description',
            'preview',
            'created_at',
            'lessons_count',
            'lessons',
        ]
