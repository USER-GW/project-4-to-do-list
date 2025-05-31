from django.contrib import admin

# Register your models here.
from .models import Category, Priority, Task

admin.site.register(Category)
admin.site.register(Priority)
admin.site.register(Task)
