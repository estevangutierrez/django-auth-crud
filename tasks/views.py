from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from .models import Task
from .forms import TaskForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':

        if request.POST['password1'] != request.POST['password2']:
            return render(request,'signup.html', {
                'form':UserCreationForm,
                'error':'Passwords Do Not Match'
            })
        
        try:
            user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
            user.save()
            login(request, user)
            return redirect('tasks')
        except:
            return render(request,'signup.html', {
                'form':UserCreationForm,
                'error':'User Already Exists'
            })

    else:
        return render(request,'signup.html', {
        'form':UserCreationForm
        })

def signin(request):
    if request.method == 'POST':
        user = authenticate(
            request, username=request.POST['username'], 
            password=request.POST['password']
            )
        
        if user is None:
            return render(request, 'signin.html', {
            'form': AuthenticationForm,
            'error':'Wrong Username or Password'
            })
        
        login(request, user)
        return redirect('tasks')
    
    else:
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })

@login_required    
def signout(request):
    logout(request)
    return redirect('home')

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user,date_completed__isnull=True)
    return render(request,'tasks.html',{'tasks':tasks})

@login_required
def completed_tasks(request):
    tasks = Task.objects.filter(user=request.user,date_completed__isnull=False).order_by('-date_completed')
    return render(request,'tasks.html',{'tasks':tasks})

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    update_form = TaskForm(instance=task)

    if request.method == 'GET':
        return render(request, 'task_detail.html', {'task':task, 'update_form':update_form})
    else:
        try:
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task':task, 'update_form':update_form, 'error':'Update task error'})
 
@login_required       
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.date_completed = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
 
@login_required      
def create_task(request):
    if request.method == 'POST':
        try:
            task = TaskForm(request.POST)
            new_task = task.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return render(request, 'create_task.html', {
                'form':TaskForm,
                'success':'Task has been created succesfully'
            })
        except ValueError:
            return render(request, 'create_task.html', {
                'form':TaskForm,
                'error':'Please type valid data'
            })
    else:
        return render(request, 'create_task.html', {
            'form':TaskForm
        })
