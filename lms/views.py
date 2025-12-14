from django.db.models import UUIDField
from django.shortcuts import render
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from users.permissions import IsOwner, IsModer
from .models import Course, Lesson, Subscription
from lms.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from .tasks import send_course_update_notifications


@extend_schema_view(
    list=extend_schema(
        summary="Получить список курсов",
    ),
    update=extend_schema(
        summary="Изменение курса по ID",
    ),
    partial_update=extend_schema(summary="Изменение какой-то части курса по ID", ),
    create=extend_schema(
        summary="Создать новый курс",
        description="При создании курса автоматически к автору привязывается пользователь который создаёт этот курс",
    ),
    retrieve=extend_schema(summary="Просмотр существующего курса по ID"),
    destroy=extend_schema(summary="Удалить курс по ID")
)
class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer

    def get_queryset(self):
        """Обычный пользователь может видеть только свои курсы. Модераторы - все"""
        user = self.request.user
        # return Course.objects.all()
        if user.groups.filter(name="Модератор").exists():
            return Course.objects.all()

        return Course.objects.filter(author=user.id)

    def perform_create(self, serializer):
        """Автоматически привязывает пользователя в качестве автора при создании курса"""
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        course = serializer.save()
        print(course.id)
        send_course_update_notifications.delay(course.id)

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, ~IsModer]
        elif self.action in ['retrieve', 'update', 'partial_update', 'list']:
            self.permission_classes = [IsAuthenticated, IsModer | IsOwner]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsOwner | ~IsModer]
        return [permission() for permission in self.permission_classes]


@extend_schema(summary="Создать новый урок")
class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModer]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@extend_schema(summary="Получить список уроков")
class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer | IsOwner]

    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name="Модератор").exists():
            return Lesson.objects.all()

        return Lesson.objects.filter(author=user)


@extend_schema(summary="Просмотр существующего урока по ID")
class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


@extend_schema(summary="Изменение урока по ID")
class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


@extend_schema(summary="Удалить урок по ID")
class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | ~IsModer]

# @extend_schema(parameters=[
#             OpenApiParameter(name='course', description='Subscription by course id', required=True, type=int,),
#         ],course=None)
class SubscriptionToggleView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course")

        if not course_id:
            return Response({"error": "course id is required"}, status=400)

        course = get_object_or_404(Course, pk=course_id)

        subs = Subscription.objects.filter(user=user, course=course)

        # Если подписка есть — удалить
        if subs.exists():
            subs.delete()
            message = "подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course)
            message = "подписка добавлена"

        return Response({"message": message})
