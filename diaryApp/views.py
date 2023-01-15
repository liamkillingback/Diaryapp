from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime, date
from .models import User, Entry, CompletedTask, Task
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import calendar
from calendar import monthrange
# Create your views here.

def index(request):
    entries = Entry.objects.filter(owner=request.user.id).order_by('-id')
    
    today = date.today()
    todays_date = today.strftime("%B %d, %Y")
    str_month, int_day, str_year = todays_date.split(' ')
    
    current_date = today.strftime("%d/%m/%Y")
    day, month, year = current_date.split('/')

    days_in_a_month = monthrange(int(year), int(month))
    page_count = days_in_a_month[1]

    paginator = Paginator(entries, page_count)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "index.html", {
        "entries": entries,
        "todays_date": todays_date,
        "page_obj": page_obj,
        "month": str_month,
        
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        main_entry = Entry.objects.get_or_create(main=True, owner=request.user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")


@csrf_exempt
def edit_post(request, id):
    entry = Entry.objects.get(pk=id)
    data = json.loads(request.body)
    body = data["body"]
    entry.body = body
    entry.save()
    return JsonResponse(entry.serialize(), safe=False)

@csrf_exempt
def update_task(request, ids):
    entry_id, task_id = ids.split(',')
    entry = Entry.objects.get(pk=entry_id)
    task = Task.objects.get(pk=task_id)

    if task in entry.completed_tasks.all():
        entry.completed_tasks.remove(task)
        entry.tasks.add(task)
    else:
        entry.completed_tasks.add(task)
        entry.tasks.remove(task)
    entry.save()
    return JsonResponse(entry.serialize(), safe=False)

@csrf_exempt
def remove_task(request, ids):
    entry_id, task_id = ids.split(',')
    entry = Entry.objects.get(pk=entry_id)
    task = Task.objects.get(pk=task_id)

    if task in entry.tasks.all():
        entry.tasks.remove(task)
    else:
        entry.completed_tasks.remove(task)
    
    entry.save()
    return JsonResponse(entry.serialize(), safe=False)

@csrf_exempt
def add_task(request, entry_id, task_name):
            
    print(entry_id)
    task_name = task_name.lower()
    entry = Entry.objects.get(pk=entry_id)
    if Task.objects.filter(task=task_name).exists():
        new_task = Task.objects.get(task=task_name)
        entry.tasks.add(new_task)
    else:
        new_task = Task(
            task=task_name
        )
        new_task.save()
        entry.tasks.add(new_task)
    entry.save()
    return JsonResponse([entry.serialize(), new_task.serialize()], safe=False)

@login_required
@csrf_exempt
def compose(request, main_id, entry_date, body):
    today = date.today()
    todays_date = today.strftime("%B %d, %Y")
    weekday = calendar.day_name[today.weekday()]

    if Entry.objects.filter(pk=main_id).exists():
        main_entry = Entry.objects.get(pk=main_id)
    else:
        main_entry = Entry(
            main = True,
            date=entry_date
        )
        main_entry.save()
    new_entry = Entry(
        body=body,
        date=entry_date,
        weekday=weekday,
        owner=request.user
    )
    new_entry.save()
    new_entry.tasks.set(main_entry.tasks.all())
    new_entry.completed_tasks.set(main_entry.completed_tasks.all())
    new_entry.save()

    main_entry.body = ""
    for task in main_entry.tasks.all():
        main_entry.tasks.remove(task)
    for task in main_entry.completed_tasks.all():
        main_entry.completed_tasks.remove(task)
    main_entry.save()

    return JsonResponse(new_entry.serialize(), safe=False)

@csrf_exempt
@login_required
def delete_entry(request, entry_id):
    entry = Entry.objects.get(pk=entry_id)
    entry.delete()
    return JsonResponse({})

@csrf_exempt
def edit_task_name(request, task_id, entry_id, new_task_name):
    # Name of new task
    new_task_name = new_task_name.lower().strip()
    # id of the entry in question, followed by the task id being changed
    entry = Entry.objects.get(pk=entry_id)
    # list of tasks in db
    all_tasks = Task.objects.all()
    completed_tasks = entry.completed_tasks.all()
    # old task
    local_task_id = task_id
    old_task = Task.objects.get(pk=local_task_id)
    print(old_task)
    entry.tasks.remove(old_task)
    entry.save()

    if Task.objects.filter(task=new_task_name).exists():
        task = Task.objects.get(task=new_task_name)
        if old_task in entry.tasks.all():
            entry.tasks.add(task)
            
            entry.save()
            print("1")
            
        else:
            entry.completed_tasks.add(task)
            entry.completed_tasks.remove(old_task)
            entry.save()
            print("2")
        return JsonResponse(task.serialize(), safe=False)
    else:
        new_task = Task(
            task=new_task_name
        )
        new_task.save()
        if old_task in entry.tasks.all():
            entry.tasks.add(new_task)
            entry.tasks.remove(old_task)
            entry.save()
            print("3")
            
        else:
            entry.completed_tasks.add(new_task)
            entry.completed_tasks.remove(old_task)
            entry.save()
            print("4")
        
        return JsonResponse(new_task.serialize(), safe=False)

    
  
    


