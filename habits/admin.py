from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('action', 'time', 'periodicity', 'created_date', 'owner', 'pk',)
    ordering = ('time',)