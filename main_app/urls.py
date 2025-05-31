from django.urls import path
from .views import HomeView, AddToDoView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('add/', AddToDoView.as_view(), name='add'),

   
]
