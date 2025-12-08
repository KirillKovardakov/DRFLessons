from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)
User = get_user_model()

@shared_task
def deactivate_inactive_users():
    """
    Деактивирует пользователей, которые не заходили более месяца.
    """
    now = timezone.now()
    one_month_ago = now - timedelta(days=30)

    inactive_users = User.objects.filter(last_login__lt=one_month_ago, is_active=True)

    count = inactive_users.update(is_active=False)
    logger.info(f"Заблокировано {count} пользователей, неактивных более месяца.")
