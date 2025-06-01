from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from .models import Category, Priority, Task
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta



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
        context['tasks'] = Task.objects.filter(due_date=selected_date).order_by('-id')
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

        category = Category.objects.filter(id=category_id).first()
        priority = Priority.objects.filter(id=priority_id).first()

        Task.objects.create(
            user=None, 
            title=title,
            description=description,
            category=category,
            priority=priority
        )

        return redirect('home')  # 


def complete_task(request, task_id):
    if request.method == 'POST':
        task = Task.objects.get(id=task_id)
        task.completed = not task.completed  # Toggle completed status
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
        task.category = Category.objects.filter(id=category_id).first()
        task.priority = Priority.objects.filter(id=priority_id).first()
        task.save()
        return redirect('home')


