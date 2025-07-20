import datetime

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

        permissions = [
            ("can_view_all_list", "Can watch all list"),
        ]


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

        permissions = [
            ("can_view_all_list", "Can watch all list"),
        ]


class Mailing(models.Model):
    start_time = models.TimeField(verbose_name="Время начала", auto_now_add=True)
    end_time = models.TimeField(verbose_name="Время окончания")
    STATUS_CHOICES = [
        ("created", "Создана"),
        ("started", "Запущена"),
        ("completed", "Завершена"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="created")
    message = models.ForeignKey(
        Letter,
        on_delete=models.SET_NULL,  # При удалении пользователя письмо остаётся
        blank=True,
        null=True,
        verbose_name="Сообщение",
    )
    clients = models.ManyToManyField(Client, verbose_name="Клиенты")
    owner = models.ForeignKey(
        AUTH_USER_MODEL,  # Используем кастомную модель пользователя
        on_delete=models.SET_NULL,  # При удалении пользователя рассылка остаётся
        blank=True,
        null=True,
        verbose_name="Создатель",
    )
    last_sent = models.DateTimeField(
        verbose_name="Последняя отправка",
        blank=True,
        null=True,
        default=datetime.datetime.now(),
    )

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"

        permissions = [
            ("can_view_all_list", "Can watch all list"),
        ]


class Logging(models.Model):
    time = models.TimeField(default=datetime.time(0, 0))
    status = models.CharField(
        choices=(
            ("success", "Успешно"),
            ("error", "Ошибка"),
        )
    )
    mailing = models.ForeignKey(
        Mailing,
        verbose_name="Рассылка",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    owner = models.ForeignKey(
        AUTH_USER_MODEL,  # Используем кастомную модель пользователя
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Создатель",
    )
    response = models.TextField(verbose_name="Ответ сервера", blank=True, null=True)

    class Meta:
        verbose_name = "Лог отправки"
        verbose_name_plural = "Логи отправки"
