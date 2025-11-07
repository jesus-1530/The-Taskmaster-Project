from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Task
from .forms import TaskForm
from django.views.decorators.csrf import csrf_exempt
import json

def task_list(request):
    tasks = Task.objects.order_by('due_date')

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()

    return render(request, 'planner/task_list.html', {'tasks': tasks, 'form': form})


def tasks_json(request):
    tasks = Task.objects.all()
    events = []

    for task in tasks:
        if task.due_date:
            events.append({
                'title': task.title,
                'start': task.due_date.strftime("%Y-%m-%dT%H:%M:%S"),
            })

    return JsonResponse(events, safe=False)

@csrf_exempt
def add_task(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        title = data.get('title')
        due_date = data.get('due_date')

        Task.objects.create(title=title, due_date=due_date)
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False})

def delete_task(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        task_id = data.get('id')
        try:
            task = Task.objects.get(id=task_id)
            task.delete()
            return JsonResponse({'success': True})
        except Task.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Task not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})
