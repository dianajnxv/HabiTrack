from django.contrib import admin

from .models import CustomUser, Category, Habit, Schedule, Task, Achievement

admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Habit)
admin.site.register(Schedule)
admin.site.register(Task)
admin.site.register(Achievement)