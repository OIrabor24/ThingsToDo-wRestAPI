from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Todo
from .forms import TodoForm


def home(request):
    return render(request, 'todo/home.html')

def signupuser(request):
    if request.method == 'GET':
     
     return render(request, 'todo/signupuser.html', {'form':UserCreationForm()})  #signup form

    else:
        if request.POST['password1'] == request.POST['password2']: #check if passwords match
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])  #create login for user
                user.save() 
                login(request, user) 
                return redirect('currenttodos')
            except IntegrityError:# checks if username has already been created, if so return signup form
                 return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error': 'That username has already been taken, please choose a new name'})  

        else:
            return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error': 'Passwords did not match'})  
            #tells user passwords did not match


def loginuser(request):
    if request.method == 'GET':
     
     return render(request, 'todo/login.html', {'form':AuthenticationForm()})  #signup form

    else:
       user = authenticate(request, username=request.POST['username'], password=request.POST['password']) 
       if user is None:
           return render(request, 'todo/login.html', {'form': AuthenticationForm(), 'error': 'Username and password did not match'})
       else:
            login(request, user) 
            return redirect('currenttodos') 

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form': TodoForm()}) 
    else:
        try:
            form = TodoForm(request.POST) #this is the returned from a user POST instance
            new_todo = form.save(commit=False) # we want to specify user field next 
            new_todo.user = request.user #we want to 
            new_todo.save()  
            return redirect('currenttodos') 
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form': TodoForm(), 'error': 'invalid data limits passed in'}) 

@login_required
def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True) #This means we only show info for the current signed in user
    return render(request, 'todo/currenttodos.html', {'todos':todos})

@login_required
def completedtodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted') 
    return render(request, 'todo/completedtodos.html', {'todos':todos})

@login_required
def viewtodo(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user) #request.user makes sure the user is the object creator.
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form}) 
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save() 
            return redirect('currenttodos') 
        except ValueError: 
            return render(request, 'todo/viewtodo.html', {'todos': todo, 'form':form, 'error': 'Invalid info!'}) 

@login_required
def completetodo(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user) 
    if request.method == 'POST':
        todo.datecompleted = timezone.now() 
        todo.save() 
        return redirect('currenttodos') 

@login_required
def deletetodo(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user) 
    if request.method == 'POST':
        todo.delete() 
        return redirect('currenttodos') 