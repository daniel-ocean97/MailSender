from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER

from .models import Logging


def send_mailing(mailing):
    """
    Отправляет рассылку всем клиентам синхронно
    """
    clients = mailing.clients.all()
    message = mailing.message

    for client in clients:
        try:
            # Отправляем письмо
            send_mail(
                subject=message.theme,
                message=message.text,
                from_email=EMAIL_HOST_USER,
                recipient_list=[client.email],
                fail_silently=False,
            )

            # Логируем успех
            Logging.objects.create(
                status="success",
                mailing=mailing,
                owner=mailing.owner,
                client=client,
                response="Письмо успешно отправлено",
            )
        except Exception as e:
            # Логируем ошибку
            Logging.objects.create(
                status="error",
                mailing=mailing,
                client=client,
                owner=mailing.owner,
                response=str(e),
            )

    # Обновляем время последней отправки
    mailing.last_sent = timezone.now()
    mailing.save()
