from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from .models import Category, Priority, Task
from django.http import HttpResponseRedirect
from django.urls import reverse



class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.all().order_by('-id')
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
            user=None,  # Or use request.user if auth is added
            title=title,
            description=description,
            category=category,
            priority=priority
        )

        return redirect('home')  # ✅ Redirect to home after task is added


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


