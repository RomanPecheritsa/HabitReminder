from rest_framework import serializers
from habits.models import Habit
from .validators import (
    validate_reward_and_related_habit,
    validate_duration,
    validate_related_habit,
    validate_pleasant_habit,
    validate_periodicity_and_weekdays,
)


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ("user",)

    def validate(self, data):
        validate_reward_and_related_habit(data)
        validate_duration(data)
        validate_related_habit(data)
        validate_pleasant_habit(data)
        validate_periodicity_and_weekdays(data, Habit.Periodicity)

        return data
