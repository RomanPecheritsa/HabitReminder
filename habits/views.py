from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from habits.models import Habit
from habits.serializers import HabitSerializer


class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = PageNumberPagination
