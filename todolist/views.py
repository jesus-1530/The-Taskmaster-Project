from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from .models import Task, UserProfile
from .canvas_api import fetch_canvas_assignments
from django.contrib import messages

@login_required(login_url='login')
def home(request):
    tasks = Task.objects.filter(user=request.user).order_by('due_date')
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        if 'add_task' in request.POST:
            Task.objects.create(
                user=request.user,
                task=request.POST.get('task'),
                task_desc=request.POST.get('task_desc'),
                due_date=request.POST.get('due_date')
            )
            return redirect('home')

        elif 'delete_task' in request.POST:
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