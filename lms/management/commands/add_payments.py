from django.core.management.base import BaseCommand
from users.models import CustomUser, Payments
from lms.models import Course, Lesson


class Command(BaseCommand):
    help = 'Add test payments to the database'

    def handle(self, *args, **kwargs):
        user, _ = CustomUser.objects.get_or_create(id=1)
        course1, _ = Course.objects.get_or_create(id=1)
        course2, _ = Course.objects.get_or_create(id=2)
        lesson1, _ = Lesson.objects.get_or_create(id=1)
        lesson2, _ = Lesson.objects.get_or_create(id=2)

        payments = [
            {"amount": "20000", "method": "cash", "user": user, "paid_course": course1},
            {"amount": "30000", "method": "transfer", "user": user, "paid_course": course2},
            {"amount": "40000", "method": "transfer", "user": user, "paid_lesson": lesson1},
            {"amount": "50000", "method": "cash", "user": user, "paid_lesson": lesson2}
        ]

        for payment_data in payments:
            payment, created = Payments.objects.get_or_create(**payment_data)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully added payment: {payment.id}'))
            else:
                self.stdout.write(
                    self.style.WARNING(f'payment already exists: {payment.id}'))
