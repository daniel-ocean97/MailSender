from django.core.mail import send_mail
from django.utils import timezone
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
                from_email=None,  # Использует DEFAULT_FROM_EMAIL из settings
                recipient_list=[client.email],
                fail_silently=False,
            )

            # Логируем успех
            Logging.objects.create(
                status='success',
                mailing=mailing,
                owner=mailing.owner,
                response='Письмо успешно отправлено'
            )
        except Exception as e:
            # Логируем ошибку
            Logging.objects.create(
                status='error',
                mailing=mailing,
                client=client,
                owner=mailing.owner,
                response=str(e)
            )

    # Обновляем время последней отправки
    mailing.last_sent = timezone.now()
    mailing.save()