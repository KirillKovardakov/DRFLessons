from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from users.permissions import IsOwner, IsModer
from .models import Course, Lesson, Subscription
from lms.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer

    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name="Модератор").exists():
            return Course.objects.all()

        return Course.objects.filter(author=user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, ~IsModer]
        elif self.action in ['retrieve', 'update', 'partial_update', 'list']:
            self.permission_classes = [IsAuthenticated, IsModer | IsOwner]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsOwner | ~IsModer]
        return [permission() for permission in self.permission_classes]


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModer]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer | IsOwner]

    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name="Модератор").exists():
            return Lesson.objects.all()

        return Lesson.objects.filter(author=user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | ~IsModer]


class SubscriptionToggleView(APIView):
    permission_classes = [IsAuthenticated]

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
