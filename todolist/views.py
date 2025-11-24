from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from .models import Task, UserProfile
from .canvas_api import fetch_canvas_assignments
from django.contrib import messages
from random import randint
from datetime import datetime, time

@login_required(login_url='login')
def home(request):
    tasks = Task.objects.filter(user=request.user).order_by('due_date')
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        if 'add_task' in request.POST:
            title = (request.POST.get('task') or '').strip()
            desc = request.POST.get('task_desc')
            due_raw = (request.POST.get('due_date') or '').strip()

            if not title:
                messages.error(request, "Task title cannot be empty.")
                return redirect('home')
            if not due_raw:
                messages.error(request, "Due date is required.")
                return redirect('home')
            # Validate & parse date (HTML date input: YYYY-MM-DD)
            try:
                date_obj = datetime.strptime(due_raw, '%Y-%m-%d').date()
            except ValueError:
                messages.error(request, "Invalid due date format.")
                return redirect('home')
            # Set due time to 23:59 for consistency and make timezone aware
            due_dt = datetime.combine(date_obj, time(23, 59))
            due_dt = timezone.make_aware(due_dt, timezone.get_current_timezone())

            random_points = randint(5, 20)
            Task.objects.create(
                user=request.user,
                task=title,
                task_desc=desc,
                due_date=due_dt,
                point_value=random_points
            )
            messages.success(request, f"Task added with {random_points} points.")
            return redirect('home')

        elif 'complete_task' in request.POST:
            task_id = request.POST.get('task_id')
            task = Task.objects.filter(id=task_id, user=request.user).first()
            if task and not task.completed:
                task.completed = True
                task.save(update_fields=['completed'])
                profile.points += task.point_value
                profile.save(update_fields=['points'])
                messages.success(request, f"Completed '{task.task}'. +{task.point_value} points!")
                Task.objects.filter(id=request.POST.get('task_id'), user=request.user).delete()
            return redirect('home')
        
    return render(request, 'home.html', {'tasks': tasks, 'profile': profile})


@login_required(login_url='login')
def sync_canvas(request):
    user = request.user
    profile, _ = UserProfile.objects.get_or_create(user=user)
    token = profile.canvas_token


    if not token:
        messages.error(request, "Canvas token not set. Please enter and save your token first.")
        return redirect('home')
    try:
        fetch_canvas_assignments(token, user)
        messages.success(request, "Canvas assignments synced successfully.")
    except Exception as e:
        messages.error(request, f"Canvas sync failed: Invalid token")
    return redirect('home')

def save_token(request):
    if request.method == "POST":
        token = request.POST.get("token")

        # Always save token for the logged-in user
        user = request.user if request.user.is_authenticated else None


        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.canvas_token = token
        profile.save()
        if token:
            messages.success(request, "Canvas token saved.")
        else:
            messages.warning(request, "Empty token submitted. Please provide a valid token.")

    return redirect('home')



def tasks_json(request):
    # Only show the logged-in user's tasks
    tasks = Task.objects.filter(user=request.user).exclude(due_date__isnull=True).order_by('due_date')
    events = []

    for t in tasks:
        dt = t.due_date

        # Convert to local timezone
        if timezone.is_aware(dt):
            dt = dt.astimezone(timezone.get_current_timezone())

        # Mark 11:59 PM deadlines as all-day
        if dt.hour == 23 and dt.minute >= 55:
            events.append({
                "title": t.task,
                "start": dt.date().isoformat(),
                "allDay": True,
            })
        else:
            events.append({
                "title": t.task,
                "start": dt.isoformat(),
                "allDay": False,
            })

    return JsonResponse(events, safe=False)


@login_required(login_url='login')
def shop(request):
    """Displays the rewards shop page where users can upload or view items."""
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'shop.html', {'profile': profile})