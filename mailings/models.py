from django.db import models

NULLABLE = {"blank": True, "null": True}

MAILING_STATUS_CHOICES = (
    ('created', 'Создана'),
    ('running', 'Запущена'),
    ('completed', 'Завершена'),
)

MAILING_PERIODICITY_CHOICES = (
    ('daily', 'Раз в день'),
    ('weekly', 'Раз в неделю'),
    ('monthly', 'Раз в месяц'),
)


class Client(models.Model):
    email = models.EmailField(verbose_name="Почта клиента")
    name = models.CharField(max_length=100, verbose_name="Имя клиента")
    comment = models.TextField(verbose_name="Комментарий", **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering = ["name"]


class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name="Тема письма")
    body = models.TextField(verbose_name="Тело письма")

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["-id"]


class Mailing(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания рассылки"
    )
    periodicity = models.CharField(max_length=50, choices=MAILING_PERIODICITY_CHOICES, verbose_name="Периодичность")
    status = models.CharField(max_length=50, choices=MAILING_STATUS_CHOICES, verbose_name="Статус рассылки")
    message = models.ForeignKey(
        Message, verbose_name="Сообщение", on_delete=models.CASCADE
    )
    clients = models.ManyToManyField(Client, verbose_name="Клиенты")

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["-created_at"]


class MailingAttempt(models.Model):
    mailing = models.ForeignKey(
        Mailing, verbose_name="Рассылка", on_delete=models.CASCADE
    )
    attempt_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата последней попытки"
    )
    status_attempt = models.BooleanField(verbose_name="Статус попытки")
    server_response = models.TextField(
        verbose_name="Ответ почтового сервиса", **NULLABLE
    )

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылок"
        ordering = ["-attempt_date"]
