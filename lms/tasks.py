from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from lms.models import Subscription
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task
def send_course_update_notifications(course_id):
    """
    Асинхронная рассылка уведомлений подписчикам курса
    """
    logger.info(f"Запущена рассылка для курса #{course_id}")
    subscriptions = Subscription.objects.filter(course_id=course_id).select_related("user")


    for sub in subscriptions:
        user = sub.user
        logger.info(f"рассылка на почту #{user.email}")

        send_mail(
            subject="Обновление курса",
            message=f"Курс, на который вы подписаны, был обновлён. ID курса: {course_id}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )


