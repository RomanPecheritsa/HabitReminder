from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models


class Habit(models.Model):
    """Модель универсальной привычки с поддержкой периодичности"""

    class Periodicity(models.TextChoices):
        DAILY = "DAILY", "Ежедневно"
        WEEKLY = "WEEKLY", "По дням недели"

    class WeekDays(models.IntegerChoices):
        MONDAY = 1, "Понедельник"
        TUESDAY = 2, "Вторник"
        WEDNESDAY = 3, "Среда"
        THURSDAY = 4, "Четверг"
        FRIDAY = 5, "Пятница"
        SATURDAY = 6, "Суббота"
        SUNDAY = 7, "Воскресенье"

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, verbose_name="Создатель привычки"
    )
    place = models.CharField(max_length=100, verbose_name="Место выполнения")
    time = models.TimeField(verbose_name="Время выполнения")
    action = models.TextField(verbose_name="Действие")
    is_pleasant = models.BooleanField(default=False, verbose_name="Приятная привычка")
    duration = models.PositiveIntegerField(verbose_name="Время выполнения (в секундах)")
    is_public = models.BooleanField(default=True, verbose_name="Публичная привычка")
    periodicity_type = models.CharField(
        max_length=10,
        choices=Periodicity.choices,
        default=Periodicity.DAILY,
        verbose_name="Тип периодичности",
    )
    weekdays = ArrayField(
        models.IntegerField(choices=WeekDays.choices),
        blank=True,
        null=True,
        verbose_name="Дни недели",
        help_text="Если выбрано 'По дням недели', укажите дни выполнения.",
    )
    reward = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Вознаграждение"
    )
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Связанная привычка",
        limit_choices_to={"is_pleasant": True},
    )

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ("id",)

    def __str__(self):
        return (
            f"{'Приятная' if self.is_pleasant else 'Полезная'} привычка: {self.action}"
        )

    def clean(self):
        if self.reward and self.related_habit:
            raise ValidationError(
                "Нельзя указать одновременно и вознаграждение, и связанную привычку"
            )

        if self.duration and self.duration > 120:
            raise ValidationError("Время выполнения не может превышать 120 секунд")

        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError(
                "Связанной привычкой может быть только приятная привычка"
            )

        if self.is_pleasant and (self.reward or self.related_habit):
            raise ValidationError(
                "Приятная привычка не может иметь вознаграждение или связанную привычку"
            )

        if self.periodicity_type == self.Periodicity.WEEKLY and (
            not self.weekdays or len(self.weekdays) < 1
        ):
            raise ValidationError(
                "Привычка должна выполняться хотя бы раз в 7 дней. Укажите дни недели"
            )

        if self.periodicity_type == self.Periodicity.DAILY and self.weekdays:
            raise ValidationError("Для ежедневной привычки дни недели не указываются")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
