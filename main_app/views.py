from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from .models import Category, Priority, Task
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta, datetime
from collections import Counter


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date_str = self.request.GET.get('date')
        if date_str:
            selected_date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
        else:
            selected_date = timezone.now().date()
        context['selected_date'] = selected_date
        context['tasks'] = Task.objects.filter(date=selected_date).order_by('-id')
        context['prev_date'] = selected_date - timedelta(days=1)
        context['next_date'] = selected_date + timedelta(days=1)
        return context


class AddToDoView(View):
    template_name = 'add.html'

    def get(self, request):
        categories = Category.objects.all()
        priorities = Priority.objects.all()
        return render(request, self.template_name, {
            'categories': categories,
            'priorities': priorities,
        })

    def post(self, request):
        title = request.POST.get('title')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        priority_id = request.POST.get('priority')
        date_str = request.POST.get('date')

        # ✅ Convert string date to Python date object
        task_date = None
        if date_str:
            try:
                task_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                task_date = timezone.now().date()

        category = Category.objects.filter(id=category_id).first()
        priority = Priority.objects.filter(id=priority_id).first()

        Task.objects.create(
            user=None,
            title=title,
            description=description,
            category=category,
            priority=priority,
            date=task_date  # ✅ Save selected date
        )

        return redirect('home')


def complete_task(request, task_id):
    if request.method == 'POST':
        task = Task.objects.get(id=task_id)
        task.completed = not task.completed
        task.save()
    return HttpResponseRedirect(reverse('home'))


def delete_task(request, task_id):
    if request.method == 'POST':
        task = Task.objects.get(id=task_id)
        task.delete()
    return HttpResponseRedirect(reverse('home'))


class EditToDoView(View):
    template_name = 'add.html'

    def get(self, request, task_id):
        task = Task.objects.get(id=task_id)
        categories = Category.objects.all()
        priorities = Priority.objects.all()
        return render(request, self.template_name, {
            'task': task,
            'categories': categories,
            'priorities': priorities,
        })

    def post(self, request, task_id):
        task = Task.objects.get(id=task_id)
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        category_id = request.POST.get('category')
        priority_id = request.POST.get('priority')
        date_str = request.POST.get('date')

        task.category = Category.objects.filter(id=category_id).first()
        task.priority = Priority.objects.filter(id=priority_id).first()

      
        if date_str:
            try:
                task.date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                pass

        task.save()
        return redirect('home')


class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
       
        date_str = self.request.GET.get('date')
        if date_str:
            selected_date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
        else:
            selected_date = timezone.now().date()
        context['selected_date'] = selected_date

        tasks = Task.objects.filter(date=selected_date).order_by('-id')
        context['tasks'] = tasks

        completed_tasks = tasks.filter(completed=True)
        completed_category_list = [str(t.category) for t in completed_tasks if t.category]
        completed_category_counts = Counter(completed_category_list)
        context['completed_category_labels'] = list(completed_category_counts.keys())
        context['completed_category_data'] = list(completed_category_counts.values())

        # For navigation
        context['prev_date'] = selected_date - timedelta(days=1)
        context['next_date'] = selected_date + timedelta(days=1)
        return context
