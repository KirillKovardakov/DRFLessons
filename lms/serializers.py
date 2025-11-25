from rest_framework.serializers import ModelSerializer, SerializerMethodField, URLField

from .models import Course, Lesson, Subscription
from .validators import validate_youtube_url


class LessonSerializer(ModelSerializer):
    video_url = URLField(
        required=False,
        allow_null=True,
        validators=[validate_youtube_url]
    )

    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ['author']


class LessonsByCourseSerializer(ModelSerializer):
    video_url = URLField(
        required=False,
        allow_null=True,
        validators=[validate_youtube_url]
    )

    class Meta:
        model = Lesson
        fields = ['id', 'name', 'description', 'preview', 'video_url', 'author']
        read_only_fields = ['author']


class CourseSerializer(ModelSerializer):
    lessons_count = SerializerMethodField()
    lessons = LessonsByCourseSerializer(many=True, read_only=True)
    is_subscribed = SerializerMethodField()

    def get_lessons_count(self, obj):
        """Считаем количество уроков в одном курсе"""
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        """
        Проверяем: есть ли у пользователя подписка на курс
        """
        user = self.context["request"].user
        if not user.is_authenticated:
            return False

        return Subscription.objects.filter(user=user, course=obj).exists()

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
            'author',
            'is_subscribed',
        ]
        read_only_fields = ['author']


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"
