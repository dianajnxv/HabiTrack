import json
import os
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q, Count
from django.db import models
from django.utils.dateformat import format
from datetime import date, timedelta
from functools import wraps
from django.core.exceptions import ValidationError

from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import CustomUser, Progress, Habit, Statistic, Category

ALLOWED_EXTENSIONS = ['.png', '.jpg', '.jpeg']
MAX_IMAGE_SIZE = 10 * 1024 * 1024 # 10mb

def validate_avatar(file):
    extension = os.path.splitext(file.name)[1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise ValidationError(f'Unsupported file format. Allowed formats: {", ".join(ALLOWED_EXTENSIONS)}')

    if file.size > MAX_IMAGE_SIZE:
        raise ValidationError(f'File size exceeds the maximum allowed size of {MAX_IMAGE_SIZE / 1024 / 1024} MB.')

def user_is_owner(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        username = kwargs.get('username')
        if request.user.username != username:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

def get_monthly_activity(user, year, month):
    # Отримуємо перший і останній день місяця
    start_date = date(year, month, 1)
    end_date = (start_date + timedelta(days=31)).replace(day=1) - timedelta(days=1)

    # Фільтруємо записи прогресу за конкретний місяць і групуємо за датою
    progress_data = (
        Progress.objects.filter(
            user=user,
            date__range=(start_date, end_date),
            status='completed'
        )
        .values('date')
        .annotate(activity_count=Count('id'))
        .order_by('date')
    )

    # Формуємо словник з активністю для кожного дня
    activity = {day: 0 for day in range(1, end_date.day + 1)}
    for record in progress_data:
        activity[record['date'].day] = record['activity_count']

    return activity

def home_view(request):
    context = {'category_list': Category.objects.all()}
    if request.user.is_authenticated:
        context['theme'] = request.user.theme
    return render(request, 'home.html', context)

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required(login_url='login')
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    return render(request, 'logout.html')

def profile_view(request, username):
    user = get_object_or_404(CustomUser, username=username)

    # Дані для графіка Success Rate
    success_rate_data = Progress.objects.filter(user_id=user.id).aggregate(
        done=Count('id', filter=Q(status='completed')),
        missed=Count('id', filter=Q(status='not_completed')),
        skipped=Count('id', filter=Q(status='skipped'))
    )

    # Дані для кругової діаграми розподілу звичок
    habits_data = Habit.objects.filter(user_id=user.id).values('category__name').annotate(count=Count('id'))

    # Дані для графіку статистики виконання звичок
    statistics_data = Statistic.objects.filter(user_id=user.id).values('habit__name', 'completed', 'total')

    activity = get_monthly_activity(user, timezone.now().year, timezone.now().month)
    dates = [f"2025-01-{day:02d}" for day in range(1, 32)]
    activity_values = [activity.get(day, 0) for day in range(1, 32)]


    context = {
        'user': user,
        'success_rate_data': success_rate_data,
        'habits_data': list(habits_data),
        'habits_count': len(habits_data),
        'statistics_data': list(statistics_data),
        'activity_data': {
            "labels": dates,
            "data": activity_values,
        },
    }

    return render(request, 'profile.html', context)

@login_required(login_url='login')
@user_is_owner
def edit_profile_view(request, username):
    user = get_object_or_404(CustomUser, username=username)

    if request.method == 'POST':
        if request.POST.get('_method') == 'PUT':
            try:
                new_username = request.POST.get('new_username', user.username)
                if not new_username:
                    return JsonResponse({
                        'status': 'error',
                        'username_error': 'This field is required.',
                    })
                new_bio = request.POST.get('bio', user.bio)

                if CustomUser.objects.filter(username=new_username).exists() and new_username != username and len(new_bio) > 250:
                    return JsonResponse({
                        'status': 'error',
                        'username_error': 'Username already exists, try another one.',
                        'bio_error': f'This field is too long. Max 250 characters but in your bio - {len(new_bio)}'
                    })
                elif CustomUser.objects.filter(username=new_username).exists() and new_username != username:
                    return JsonResponse({
                        'status': 'error',
                        'username_error': 'Username already exists, try another one.'
                    })
                elif len(new_bio) > 250:
                    return JsonResponse({
                        'status': 'error',
                        'bio_error': f'This field is too long. Max 250 characters but in your bio - {len(new_bio)}'
                    })

                user.username = new_username
                user.bio = new_bio

                if 'avatar' in request.FILES:
                    avatar = request.FILES['avatar']
                    try:
                        validate_avatar(avatar)
                        user.avatar = avatar
                    except ValidationError as e:
                        return JsonResponse({
                            'status': 'error',
                            'avatar_error': e.message
                        })

                user.save()
                return JsonResponse({"status": "success", "message": "Profile updated", "redirect_url": f'/profile/{user.username}'})

            except json.JSONDecodeError:
                return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)


@csrf_exempt
def change_theme(request):
    if request.method == "POST" and request.user.is_authenticated:
        theme = request.POST.get("theme")  # Отримуємо тему з POST-запиту
        if theme in ["light", "dark", "motivating"]:  # Перевіряємо, чи тема допустима
            request.user.theme = theme
            request.user.save()
            return JsonResponse({"status": "success", "message": "Theme updated successfully."})
        return JsonResponse({"status": "error", "message": "Invalid theme selected."}, status=400)
    return JsonResponse({"status": "error", "message": "Unauthorized or invalid request."}, status=401)

#creating a habit
@csrf_exempt
def create_habit_view(request):
    if request.method == "POST" and request.user.is_authenticated:
        try:
            if not request.body:
                return JsonResponse({'success': False, 'error': 'Empty request body'})

            data = json.loads(request.body)
            name = data.get('name')
            category_id = data.get('category')
            days = data.get('days')
            priority = data.get('priority')

            new_habit = Habit.objects.create(
                name=name,
                category_id=category_id,
                frequency=days,  
                priority=priority,
                user_id=request.user.id,
                created_at=timezone.now(),
            )

            return JsonResponse({'success': True})  

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON format'})

        except Exception as e:
            print(e)
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid method'})



#subscribe
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from .forms import SubscribeForm

def subscribe_view(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        
        if form.is_valid():  # Якщо форма валідна
            email = form.cleaned_data['email']
            # Відправка email
            send_mail(
                'Thank you for subscribing!',
                'You will receive updates from us soon.',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return redirect('subscribe-success')  # Перенаправлення на сторінку успіху
        else:  # Якщо форма не валідна
            # Залишити користувача на тій самій сторінці з помилками
            return render(request, 'home.html', {'form': form})
    else:
        form = SubscribeForm()
    
    return render(request, 'home.html', {'form': form})

#schedule
from django.shortcuts import render, get_object_or_404, redirect
from .models import Habit
from .forms import HabitForm
from django.contrib.auth.decorators import login_required

@login_required
def schedule(request):
    habits = Habit.objects.filter(user=request.user)
    return render(request, 'schedule.html', {'habits': habits})

@login_required
def habit_delete(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    if request.method == 'POST':
        habit.delete()
    return redirect('schedule')

@login_required
def habit_edit(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    if request.method == 'POST':
        form = HabitForm(request.POST, instance=habit)
        if form.is_valid():
            form.save()
            return redirect('schedule')
    else:
        form = HabitForm(instance=habit)
    return render(request, 'habit_edit.html', {'form': form})

@login_required
def toggle_status(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    if request.method == 'POST':
        next_status = {'not_done': 'done', 'done': 'missed', 'missed': 'not_done'}
        habit.status = next_status.get(habit.status, 'not_done')
        habit.save()
    return redirect('schedule')

#back home
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')


#calendar
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import json
from .models import Task
from datetime import datetime

@login_required
def get_tasks(request):
    if request.method == 'GET':
        tasks = Task.objects.filter(user=request.user)  # Обмежуємо по користувачу
        data = [{
            'id': task.id,
            'title': task.title,
            'date': task.date.isoformat()
        } for task in tasks]
        return JsonResponse(data, safe=False)
    return HttpResponseNotAllowed(['GET'])


@login_required
def add_task(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            title = data.get('title')
            date_str = data.get('date')
            if not title or not date_str:
                return JsonResponse({'status': 'error', 'message': 'Title and date are required'}, status=400)

            # Перетворення рядка у дату
            try:
                date_obj = datetime.fromisoformat(date_str).date()  # приймає формат ISO з часом або без
            except ValueError:
                return JsonResponse({'status': 'error', 'message': 'Invalid date format, expected YYYY-MM-DD'}, status=400)

            task = Task.objects.create(title=title, date=date_obj, user=request.user)
            return JsonResponse({
                'status': 'success',
                'id': task.id,
                'title': task.title,
                'date': task.date.isoformat()
            })
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    return HttpResponseNotAllowed(['POST'])


@login_required
def schedule_page(request):
    return render(request, 'schedule.html')

@login_required
def delete_task(request, task_id):
    if request.method == 'DELETE':
        try:
            task = Task.objects.get(id=task_id, user=request.user)
            task.delete()
            return JsonResponse({'status': 'success'})
        except Task.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Task not found'}, status=404)
    return HttpResponseNotAllowed(['DELETE'])

@login_required
def edit_task(request, task_id):
    if request.method == 'PUT':
        try:
            task = Task.objects.get(id=task_id, user=request.user)
        except Task.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Task not found'}, status=404)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

        new_title = data.get('title', '').strip()
        if not new_title:
            return JsonResponse({'status': 'error', 'message': 'Title cannot be empty'}, status=400)

        task.title = new_title
        task.save()
        return JsonResponse({'status': 'success'})
    return HttpResponseNotAllowed(['PUT'])
