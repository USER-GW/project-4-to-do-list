from django.urls import path
from .views import HomeView, AddToDoView, complete_task, delete_task, EditToDoView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('add/', AddToDoView.as_view(), name='add'),
    path('complete-task/<int:task_id>/', complete_task, name='complete_task'),
    path('delete-task/<int:task_id>/', delete_task, name='delete_task'),
    path('edit-task/<int:task_id>/', EditToDoView.as_view(), name='edit_task'),
]
