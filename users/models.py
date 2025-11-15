from django.db import models
from django.contrib.auth.models import AbstractUser
from lms.models import Course, Lesson


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Почта', help_text='Укажите свою почту')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    avatar = models.ImageField(upload_to='users/avatars/', blank=True, null=True)
    country = models.CharField(verbose_name='Страна', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Payments(models.Model):
    PAYMENT_METHODS = (
        ("cash", "Наличные"),
        ("transfer", "Перевод на счет"),
    )

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='users',
        verbose_name="Пользователь"
    )
    created_at = models.DateField(verbose_name='Дата оплаты', auto_now_add=True)

    paid_course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Оплаченный курс",
        related_name="course_payments"
    )

    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Оплаченный урок",
        related_name="lesson_payments"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма оплаты")

    method = models.CharField(max_length=20, choices=PAYMENT_METHODS, verbose_name="Способ оплаты")

    def __str__(self):
        item = self.paid_course or self.paid_lesson
        return f"Оплата {self.user.email} — {item} на сумму {self.amount}"

    class Meta:
        verbose_name = "Платёж"
        verbose_name_plural = "Платежи"
