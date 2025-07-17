from django.db import models

from config.settings import AUTH_USER_MODEL

class Client(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150)
    comment = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(
        AUTH_USER_MODEL,  # Используем кастомную модель пользователя
        blank=True,
        null=True,
        on_delete=models.SET_NULL,  # При удалении пользователя клиент остаётся
        verbose_name="Создатель",
    )

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"



class Letter(models.Model):
    theme = models.CharField(max_length=150)
    text = models.TextField()
    owner = models.ForeignKey(
        AUTH_USER_MODEL,  # Используем кастомную модель пользователя
        on_delete=models.SET_NULL,  # При удалении пользователя письмо остаётся
        blank=True,
        null=True,
        verbose_name="Создатель",
    )

    def __str__(self):
        return self.theme

    class Meta:
        verbose_name = "Письмо"
        verbose_name_plural = "Письма"

class Mailing(models.Model):
    start_time = models.DateTimeField(verbose_name="Время начала", auto_now_add=True)
    end_time = models.DateTimeField(verbose_name="Время окончания")
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('completed', 'Завершена'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='created'
    )
    message = models.ForeignKey(Letter, on_delete=models.SET_NULL,  # При удалении пользователя письмо остаётся
        blank=True,
        null=True,
        verbose_name="Сообщение")
    clients = models.ManyToManyField(Client, verbose_name="Клиенты")
    owner = models.ForeignKey(
        AUTH_USER_MODEL,  # Используем кастомную модель пользователя
        on_delete=models.SET_NULL,  # При удалении пользователя рассылка остаётся
        blank=True,
        null=True,
        verbose_name="Создатель",
    )

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"


class Logging(models.Model):
    time = models.DateTimeField
    status = models.CharField(choices=(("success", "Успешно"), ("error", "Ошибка"),))
    mailing = models.ForeignKey(Mailing, verbose_name="Рассылка", on_delete=models.SET_NULL, blank=True,
        null=True)
    owner = models.ForeignKey(
        AUTH_USER_MODEL,  # Используем кастомную модель пользователя
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Создатель",
    )


