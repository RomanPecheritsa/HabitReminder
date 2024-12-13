from rest_framework import serializers


def validate_reward_and_related_habit(data):
    if data.get("reward") and data.get("related_habit"):
        raise serializers.ValidationError(
            "Нельзя указать одновременно и вознаграждение, и связанную привычку"
        )


def validate_duration(data):
    duration = data.get("duration")
    if duration and duration > 120:
        raise serializers.ValidationError(
            {"duration": "Время выполнения не может превышать 120 секунд"}
        )


def validate_related_habit(data):
    related_habit = data.get("related_habit")
    if related_habit and not related_habit.is_pleasant:
        raise serializers.ValidationError(
            {
                "related_habit": "Связанной привычкой может быть только приятная привычка"
            }
        )


def validate_pleasant_habit(data):
    if data.get("is_pleasant") and (
        data.get("reward") or data.get("related_habit")
    ):
        raise serializers.ValidationError(
            "Приятная привычка не может иметь вознаграждение или связанную привычку"
        )


def validate_periodicity_and_weekdays(data, periodicity_type_enum):
    periodicity_type = data.get("periodicity_type")
    weekdays = data.get("weekdays")
    if periodicity_type == periodicity_type_enum.WEEKLY:
        if not weekdays or len(weekdays) < 1:
            raise serializers.ValidationError(
                {
                    "weekdays": "Привычка должна выполняться хотя бы раз в 7 дней. Укажите дни недели"
                }
            )
    elif periodicity_type == periodicity_type_enum.DAILY and weekdays is not None:
        raise serializers.ValidationError(
            {"weekdays": "Для ежедневной привычки дни недели не указываются"}
        )
