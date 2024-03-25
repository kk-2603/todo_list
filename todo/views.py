from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task, Category
from django.contrib.auth.forms import UserCreationForm
from .forms import TaskForm
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.oauth2.views import OAuth2Adapter, OAuth2LoginView
from django.urls import reverse

class GoogleLogin(OAuth2LoginView):
    adapter_class = GoogleOAuth2Adapter

    def get_callback_url(self, request, app):
        callback_url = reverse("socialaccount:google_login_callback")
        return request.build_absolute_uri(callback_url)

def google_login(request):
    return redirect(reverse("socialaccount:google_login"))

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
    
@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'todo/task_list.html', {'tasks': tasks})

@login_required
def task_create(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            category_id = request.POST.get('category')
            task.category_id = category_id
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'todo/task_form.html', {'form': form, 'categories': categories})

@login_required
def task_update(request, task_id):
    print("Inside task_update view")  # Print to check if view is being accessed
    task = get_object_or_404(Task, id=task_id)
    categories = Category.objects.all()

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        print("Received GET request")  # Print to check if GET request is received
        form = TaskForm(instance=task)

    return render(request, 'todo/task_form.html', {'form': form, 'categories': categories, 'task': task})

@login_required
def task_delete(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'todo/task_confirm_delete.html', {'task': task})


def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')  # Redirect to the task list page
    else:
        form = CategoryForm()
    return render(request, 'create_category.html', {'form': form})


def dashboard(request):
    tasks_due_soon = Task.objects.filter(due_date__lte=timezone.now() + timezone.timedelta(days=1))
    return render(request, 'dashboard.html', {'tasks_due_soon': tasks_due_soon})    