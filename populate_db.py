import random
from django.utils.timezone import now, timedelta
from service.models import (  # Замість `myapp` вкажіть вашу назву додатку
    CustomUser, Category, Habit, Subcategory, Schedule, Reminder, Progress,
    Achievement, Statistic, MotivationQuote, Theme
)

# Очистити таблиці перед заповненням
def clear_database():
    Progress.objects.all().delete()
    Reminder.objects.all().delete()
    Schedule.objects.all().delete()
    Subcategory.objects.all().delete()
    Habit.objects.all().delete()
    Category.objects.all().delete()
    Achievement.objects.all().delete()
    Statistic.objects.all().delete()
    CustomUser.objects.all().delete()
    Theme.objects.all().delete()
    MotivationQuote.objects.all().delete()

def populate_database():
    # Створення користувачів
    users = [
        CustomUser.objects.create_user(
            username=f"user{i}",
            email=f"user{i}@example.com",
            password="password123",
            theme=random.choice(['light', 'dark', 'motivating'])
        ) for i in range(1, 11)
    ]

    # Створення категорій
    categories = [
        Category.objects.create(name=name, description=f"{name} description")
        for name in ["Health", "Productivity", "Learning", "Hobbies"]
    ]

    # Створення звичок
    habits = []
    for user in users:
        for _ in range(3):  # Кожен користувач матиме по 3 звички
            category = random.choice(categories)
            habit = Habit.objects.create(
                user=user,
                name=f"Habit {random.randint(1, 100)}",
                category=category,
                priority=random.choice(['low', 'medium', 'high']),
                frequency=random.sample(['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'], 3)
            )
            habits.append(habit)

    # Створення підкатегорій
    subcategories = [
        Subcategory.objects.create(
            user=random.choice(users),
            habit=random.choice(habits),
            name=f"Subcategory {i}"
        ) for i in range(10)
    ]

    # Створення розкладу
    schedules = [
        Schedule.objects.create(
            user=random.choice(users),
            habit=random.choice(habits),
            date=now().date() + timedelta(days=random.randint(0, 10)),
            time=(now() + timedelta(hours=random.randint(0, 23))).time()
        ) for _ in range(15)
    ]

    # Створення нагадувань
    reminders = [
        Reminder.objects.create(
            schedule=random.choice(schedules),
            email=f"reminder{i}@example.com",
            status=random.choice(['active', 'inactive'])
        ) for i in range(10)
    ]

    # Прогрес
    progress = [
        Progress.objects.create(
            user=random.choice(users),
            habit=random.choice(habits),
            date=now().date() - timedelta(days=random.randint(0, 7)),
            status=random.choice(['completed', 'not_completed', 'skipped'])
        ) for _ in range(20)
    ]

    # Досягнення
    achievements = [
        Achievement.objects.create(
            user=random.choice(users),
            name=f"Achievement {i}",
            description=f"Description of Achievement {i}"
        ) for i in range(5)
    ]

    # Статистика
    statistics = [
        Statistic.objects.create(
            user=random.choice(users),
            habit=random.choice(habits),
            period=timedelta(days=7),
            completed=random.randint(0, 10),
            total=10
        ) for _ in range(10)
    ]

    # Цитати для мотивації
    quotes = [
        MotivationQuote.objects.create(
            text=f"Motivation Quote {i}",
            author=f"Author {i}"
        ) for i in range(10)
    ]

    # Теми
    themes = [
        Theme.objects.create(
            name=f"Theme {i}",
            style=f".theme-{i} {{ background-color: #{random.randint(0, 0xFFFFFF):06x}; }}"
        ) for i in range(3)
    ]

    print("Database populated successfully!")

# Виконати функції
clear_database()
populate_database()