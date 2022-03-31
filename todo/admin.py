from django.contrib import admin
from .models import Todo
# Register your models here.


class TodoAdmin(admin.ModelAdmin):
    fields = ['title', 'memo', 'datecompleted', 'created', 'important', 'user'] 
    readonly_fields = ('created',)  

admin.site.register(Todo, TodoAdmin) 