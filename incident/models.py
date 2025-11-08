from django.db import models


class Incident(models.Model):
    class IncidentSource(models.TextChoices):
        OPERATOR = 'operator', 'Оператор'
        MONITORING = 'monitoring', 'Мониторинг'
        PARTNER = 'partner', 'Партнёр'

    class IncidentStatus(models.TextChoices):
        OPEN = 'open', 'Открыт'
        IN_PROGRESS = 'in_progress', 'В работе'
        RESOLVED = 'resolved', 'Решён'
        CLOSED = 'closed', 'Закрыт'

    description = models.TextField(
        'Описание',
        help_text='Текст/описание инцидента'
    )

    status = models.CharField(
        'Статус',
        max_length=20,
        choices=IncidentStatus.choices,
        default=IncidentStatus.OPEN
    )

    source = models.CharField(
        'Источник',
        max_length=20,
        choices=IncidentSource.choices
    )

    created_at = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Время обновления'
    )

    class Meta:
        verbose_name = 'Инцидент'
        verbose_name_plural = 'Инциденты'
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=['status'], name='status'),
        ]

    def __str__(self):
        return f'Инцидент #{self.id} от {self.source} в статусе: {self.status}'
