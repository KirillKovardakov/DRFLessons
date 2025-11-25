from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

from users.models import CustomUser
from lms.models import Course, Subscription, Lesson

User = get_user_model()


class SubscriptionTests(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="test@example.com", password="123456", username='TestSubscriptionUser'
        )

        self.course = Course.objects.create(
            name="Test Course",
            description="Desc",
            author=self.user
        )

        self.url = reverse("lms:subscription")

    def test_subscribe(self):
        """
        Пользователь может подписаться на курс.
        """
        self.client.force_authenticate(user=self.user)

        response = self.client.post(self.url, {"course": self.course.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "подписка добавлена")

        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

    def test_unsubscribe(self):
        """
        При повторном запросе — подписка удаляется.
        """
        self.client.force_authenticate(self.user)

        Subscription.objects.create(user=self.user, course=self.course)

        response = self.client.post(self.url, {"course": self.course.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "подписка удалена")

        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

    def test_unauthenticated_user_cannot_subscribe(self):
        """
        Неавторизованному пользователю подписка недоступна.
        """
        response = self.client.post(self.url, {"course": self.course.id})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_subscribe_to_nonexistent_course(self):
        """
        Ошибка при попытке подписаться на несуществующий курс.
        """
        self.client.force_authenticate(self.user)

        response = self.client.post(self.url, {"course": 999})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_course_serializer_shows_subscription_flag(self):
        """
        Сериализатор курса должен показывать is_subscribed = True,
        если текущий пользователь подписан.
        """
        self.client.force_authenticate(self.user)

        Subscription.objects.create(user=self.user, course=self.course)

        detail_url = reverse("lms:course-detail", args=[self.course.id])

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("is_subscribed", response.data)
        self.assertTrue(response.data["is_subscribed"])

    def test_course_serializer_shows_no_subscription(self):
        """
        Если пользователь не подписан — is_subscribed=False.
        """
        self.client.force_authenticate(self.user)

        detail_url = reverse("lms:course-detail", args=[self.course.id])

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["is_subscribed"])


class LessonTests(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="test@example.com", password="123456", username='TestLessonUser'
        )

        self.manager_group, created = Group.objects.get_or_create(name="Модератор")
        self.manager = User.objects.create_user(
            email="manager@test.com",
            password="testpass123",
            username="TestLessonManager"
        )
        self.manager.groups.add(self.manager_group)
        self.manager.save()

        self.lesson = Lesson.objects.create(
            name="Test Lesson",
            description="Desc",
            author=self.user
        )

    def test_lesson_user_retrieve(self):
        """Пользователь может просматривать свой урок"""
        self.url = reverse("lms:lesson-get", args=(self.lesson.pk,))
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('name'), 'Test Lesson')

    def test_lesson_manager_retrieve(self):
        """Модератор может просматривать все уроки"""
        self.url = reverse("lms:lesson-get", args=(self.lesson.pk,))
        self.client.force_authenticate(user=self.manager)

        response = self.client.get(self.url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('name'), 'Test Lesson')

    def test_lesson_user_create(self):
        """Пользователь может создать урок"""
        self.url = reverse("lms:lesson-create")
        self.client.force_authenticate(user=self.user)

        data = {"name": "Test create Lesson", "description": "Desc"}
        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Lesson.objects.filter(name="Test create Lesson").exists())

    def test_lesson_manager_create(self):
        """Модератор не может создавать уроки"""
        self.url = reverse("lms:lesson-create")
        self.client.force_authenticate(user=self.manager)

        data = {"name": "Test create Lesson", "description": "Desc"}
        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_user_update(self):
        """Пользователь может редактировать свой урок"""
        self.url = reverse("lms:lesson-update", args=(self.lesson.pk,))
        self.client.force_authenticate(user=self.user)

        data = {"name": "Test update Lesson", "description": "Desc updated"}

        response = self.client.patch(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Lesson.objects.filter(name="Test update Lesson", description="Desc updated").exists())

    def test_lesson_manager_update(self):
        """Модератор может редактировать уроки"""
        self.url = reverse("lms:lesson-update", args=(self.lesson.pk,))
        self.client.force_authenticate(user=self.manager)

        data = {"name": "Test update Lesson", "description": "Desc updated"}

        response = self.client.patch(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Lesson.objects.filter(name="Test update Lesson", description="Desc updated").exists())

    def test_lesson_user_delete(self):
        """Пользователь может удалить свой урок"""
        self.url = reverse("lms:lesson-delete", args=(self.lesson.pk,))
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())

    def test_lesson_manager_delete(self):
        """Модератор не может удалять чужие уроки"""
        self.url = reverse("lms:lesson-delete", args=(self.lesson.pk,))
        self.client.force_authenticate(user=self.manager)

        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Lesson.objects.filter(id=self.lesson.id).exists())

    def test_lesson_user_list(self):
        """Пользователь может просматривать список уроков"""
        self.url = reverse("lms:lesson-list")
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_user_list(self):
        """Модератор может просматривать список уроков"""
        self.url = reverse("lms:lesson-list")
        self.client.force_authenticate(user=self.manager)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
