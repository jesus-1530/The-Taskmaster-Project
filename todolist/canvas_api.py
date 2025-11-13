import requests
from datetime import datetime, timedelta
import pytz
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Task, UserProfile
from django.contrib.auth.models import User

CANVAS_API_URL = "https://sjsu.instructure.com/api/v1"


@login_required(login_url='login')
def home(request):
    if request.method == 'POST':
        if 'add_task' in request.POST:
            task_name = request.POST.get('task')
            task_desc = request.POST.get('task_desc')
            due_date = request.POST.get('due_date')
            Task.objects.create(
                user=request.user,
                task=task_name,
                task_desc=task_desc,
                due_date=due_date
            )
            return redirect('home')
        elif 'delete_task' in request.POST:
            task_id = request.POST.get('task_id')
            Task.objects.filter(id=task_id, user=request.user).delete()
            return redirect('home')

    tasks = Task.objects.filter(user=request.user).order_by('due_date')
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'home.html', {'tasks': tasks, 'profile': profile})


@login_required
def sync_canvas(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    token = profile.canvas_token

    return redirect('home')


def save_token(request):
    if request.method == "POST":
        token = request.POST.get("token")

        user = request.user if request.user.is_authenticated else None

        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.canvas_token = token
        profile.save()

    return redirect('home')


def fetch_canvas_assignments(token, user):
    cutoff = timezone.now() - timedelta(days=7)
    headers = {"Authorization": f"Bearer {token}"}
    local_tz = pytz.timezone("America/Los_Angeles")

    courses_response = requests.get(
    f"{CANVAS_API_URL}/courses",
    headers=headers,
    params={"enrollment_state": "active", "state[]": ["available", "current", "future"]}
)

    courses = courses_response.json()

    profile, _ = UserProfile.objects.get_or_create(user=user)

    for course in courses:
        course_id = course.get("id")
        if not course_id:
            continue

        course_name = course.get("name", "Unknown Course")

        assignments_response = requests.get(
            f"{CANVAS_API_URL}/courses/{course_id}/assignments",
            headers=headers,
            params={"bucket": "upcoming", "include[]": ["submission"], "order_by": "due_at"}
        )

        assignments = assignments_response.json()

        for a in assignments:
            name = a["name"]
            due_raw = a.get("due_at")

            if not due_raw:
                continue

            # Convert UTC → local time
            due_utc = datetime.fromisoformat(due_raw.replace("Z", "+00:00"))
            due_local = due_utc.astimezone(local_tz)

            if due_local < cutoff.astimezone(local_tz):
                continue

            name_lower = name.lower()
            if "quiz" in name_lower:
                points = 10
            elif "exam" in name_lower or "midterm" in name_lower:
                points = 25
            elif "project" in name_lower:
                points = 20
            elif "homework" in name_lower or "hw" in name_lower:
                points = 8
            else:
                points = 5

            task_obj, created = Task.objects.update_or_create(
                user=user,
                task=name,
                defaults={
                    "task_desc": f"From Canvas - {course_name}",
                    "due_date": due_local,
                    "point_value": points,
                }
            )

            submission = a.get("submission", {})
            is_done = submission.get("workflow_state") in ["graded", "submitted"]

            if is_done and not getattr(task_obj, "completed", False):
                task_obj.completed = True
                task_obj.save()
                profile.points += task_obj.point_value
                profile.save()
