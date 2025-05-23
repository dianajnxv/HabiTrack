import random
from django.db import models
from django.contrib.auth.models import AbstractUser

# Theme Choices for user interface customization
class ThemeChoices(models.TextChoices):
    LIGHT = "light", "Light Theme"
    DARK = "dark", "Dark Theme"
    MOTIVATING = "motivating", "Motivating Theme"

# Custom User Model
class CustomUser(AbstractUser):
    bio = models.TextField(
        blank=True,
        verbose_name='Bio',
        help_text='Enter your bio',
        max_length=250
    )
    email = models.EmailField(
        unique=True,
        verbose_name="Email Address",
        help_text="Enter a unique email address.",
        db_index=True
    )
    google_calendar_integration = models.BooleanField(
        default=False,
        verbose_name="Google Calendar Integration",
        help_text="Enable or disable Google Calendar integration."
    )
    theme = models.CharField(
        max_length=20,
        choices=ThemeChoices.choices,
        default=ThemeChoices.LIGHT,
        verbose_name="Theme",
        help_text="Select a theme for your interface."
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        default='avatars/avatar.jpg',
        verbose_name="Avatar",
        help_text="Upload a profile picture."
    )
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.'
    )

    class Meta:
        verbose_name = "Custom User"
        verbose_name_plural = "Custom Users"

    def __str__(self):
        return self.username

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Category Name")
    description = models.TextField(blank=True, null=True, verbose_name="Description")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

# Habit Model (merged definition)
class Habit(models.Model):
    DAYS_OF_WEEK = [
        ('mon', 'Monday'),
        ('tue', 'Tuesday'),
        ('wed', 'Wednesday'),
        ('thu', 'Thursday'),
        ('fri', 'Friday'),
        ('sat', 'Saturday'),
        ('sun', 'Sunday'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='habits')
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        related_name='habits',
        verbose_name="Category",
        help_text="Select a category for this habit."
    )
    priority = models.CharField(
        max_length=10,
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
        default='medium',
        verbose_name="Priority"
    )
    frequency = models.JSONField(
        default=list,
        verbose_name="Days of the Week",
        help_text="Select the days for this habit."
    )
    STATUS_CHOICES = [
        ('not_done', 'Not Done'),
        ('done', 'Done'),
        ('missed', 'Missed'),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='not_done',
        verbose_name='Status'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_frequency_display(self):
        day_names = dict(self.DAYS_OF_WEEK)
        return ", ".join([day_names.get(day, day) for day in self.frequency])

    
    

# # Schedule Model (merged definition)
class Schedule(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='schedules')
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='schedules')
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(
        max_length=20, 
        choices=[('completed', 'Completed'), ('not_completed', 'Not Completed'), ('skipped', 'Skipped')], 
        default='not_completed'
    )

    def __str__(self):
        return f"{self.habit.name} on {self.date} at {self.time}"

# Reminder Model
class Reminder(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='reminders')
    email = models.EmailField()
    status = models.CharField(
        max_length=10,
        choices=[('active', 'Active'), ('inactive', 'Inactive')],
        default='active'
    )

    def __str__(self):
        return f"Reminder for {self.schedule.habit.name} ({self.status})"

# Progress Model
class Progress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='progresses')
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='progresses')
    date = models.DateField()
    status = models.CharField(
        max_length=15,
        choices=[('completed', 'Completed'), ('not_completed', 'Not Completed'), ('skipped', 'Skipped')],
        default='not_completed'
    )

    def __str__(self):
        return f"{self.habit.name} on {self.date} - {self.status}"

# Achievement Model
class Achievement(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='achievements')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    earned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Statistic Model
class Statistic(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='statistics')
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='statistics')
    period = models.DurationField()
    completed = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Stats for {self.habit.name} ({self.period})"

# MotivationQuote Model
class MotivationQuote(models.Model):
    text = models.TextField()
    author = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.text

# Theme Model
class Theme(models.Model):
    name = models.CharField(max_length=50)
    style = models.TextField()

    def __str__(self):
        return self.name


#Calendar
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Task(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)                 # назва завдання
    date = models.DateField()                                 # дата завдання

    def __str__(self):
        return f"{self.title} on {self.date}"
