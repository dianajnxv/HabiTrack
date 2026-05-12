from datetime import date
from .models import Habit, Task

def daily_progress(request):
    if request.user.is_authenticated:
        today = date.today()
        day_name = today.strftime('%A').lower() 

        habits_today = Habit.objects.filter(user=request.user, frequency__icontains=day_name)
        habits_total = habits_today.count()
        
        habits_done = habits_today.filter(last_completed=today).count()

        tasks_today = Task.objects.filter(user=request.user, date=today)
        tasks_total = tasks_today.count()
        tasks_done = tasks_today.filter(is_completed=True).count()

        total = habits_total + tasks_total
        done = habits_done + tasks_done
        
        progress_percent = (done / total * 100) if total > 0 else 0
        
        return {
            'today_progress': round(progress_percent),
            'tasks_remaining': total - done
        }
    return {'today_progress': 0, 'tasks_remaining': 0}