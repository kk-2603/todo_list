# notification_logic.py
from django.utils import timezone
from django.core.mail import send_mail
from .models import Task

def send_due_date_notifications():
    """
    Sends notifications for tasks that are due soon.
    """
    tasks_due_soon = Task.objects.filter(due_date__lte=timezone.now() + timezone.timedelta(days=1))
    for task in tasks_due_soon:
        send_mail(
            'Task Due Soon',
            f'Task "{task.title}" is due soon.',
            'from@example.com',
            [task.assignee.email],
            fail_silently=False,
        )