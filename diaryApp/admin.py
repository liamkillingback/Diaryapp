from django.contrib import admin
from .models import User, Entry, Task, CompletedTask
# Register your models here.
admin.site.register(User)
admin.site.register(Entry)
admin.site.register(Task)
admin.site.register(CompletedTask)
