from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .decorators import unauthenticated_user, allowed_users, admin_only

# Create your views here.
from .models import Task, Category, CustomUserAdmin, Kin
from .forms import TaskForm, CreateUserForm, CategoryForm, ProfileForm

@unauthenticated_user
def welcome(request):
	if request.user.is_authenticated:
		return redirect('index')
		print("success")
	else:
		print("failed")
		if request.method == 'POST':
			username = request.POST.get('username')
			password = request.POST.get('password1')

			user = authenticate(request, username=username, password=password)
			print("woah")
			
			if user is not None:
				login(request, user)
				return redirect('index')
				print("yup")
			else:
				messages.info(request, 'Username OR Password is incorrect')
				print("nope")

	context = {}
	return render(request, 'welcome.html', context)

def registerPage(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			print("zxcv")
			print("Register success")
			form.save()
			user = form.cleaned_data.get('username')
			messages.success(request, "Account was created for " + user)

		else:
			print("qwerty")
			print("Register failed")
			print(form.errors)
			messages.info(request, "Could not register")
			return redirect('register')
			
		return redirect('login')

	context = {'form':form}
	return render(request, 'register.html', context)

def about(request):
	context = {}
	return render(request, 'about.html', context)

@unauthenticated_user
def loginPage(request):
	if request.user.is_authenticated:
		return redirect('index')
		print("success")
	else:
		print("failed")
		if request.method == 'POST':
			username = request.POST.get('username')
			password = request.POST.get('password1')

			user = authenticate(request, username=username, password=password)
			print("woah")
			
			if user is not None:
				login(request, user)
				return redirect('index')
				print("yup")
			else:
				messages.info(request, 'Username OR Password is incorrect')
				print("nope")

	context = {}
	return render(request, 'login.html', context)

def forgotPassword(request):
	print("Forgot")

	context = {}
	return render(request, 'forgot-password.html')


def logoutUser(request):
	print("logging out")
	logout(request)
	# Redirect to the login page
	return redirect('welcome')

# @login_required(login_url='login')
def index(request):
	
	# admin = CustomerUserAdmin.objects.all()
	# admin_form = CreateUserForm()
	
	# if group == "admin":
    # 	#print('User is Admin')
	# 	#admin_user = True
	# else:
	# 	print('User is not Admin')

	tasks = Task.objects.all()
	form = TaskForm()

	if request.method == 'POST':
		form = TaskForm(request.POST)
		print('Processing Form')
		if form.is_valid():
			print('Form Valid')
			task_obj = form.save(commit=False)
			task_obj.user = request.user
			task_obj.complete = False
			task_obj.save()
		
		else:
			print('Form Invalid')
			print(form.errors)
		return redirect('/index')
		return redirect('/index')


	context = {
		'tasks':tasks, 
		'form':form,
		#'admin_user':admin_user
		}
	return render(request, 'index.html', context)

def complete_toggle(request, todo_id):
	print('in complete toggle')
	# if request.is_ajax() and request.method=='POST':
	if request.is_ajax() and request.method=='POST':
		task_id = request.POST.get('task_id')
		task = Task.objects.get(pk=task_id)
		print('task')
		task.complete = True if task.complete == False else False
		task.save()
		data = {'status':'success', 'is_complete': task.complete}
		return JsonResponse(data, status=200)
	else:
		data = {'status':'error'}
		return JsonResponse(data, status=400)

@login_required(login_url='login')
def updateTask(request, pk):
	
	task = Task.objects.get(id=pk)	

	if request.method == 'POST':
		form = TaskForm(request.POST, instance=task)
		if form.is_valid():
			form.save()
			return redirect('/index')

	form = TaskForm(instance=task)
	context = {'form':form}

	return render(request, 'update.html', context)

@login_required(login_url='login')
def deleteTask(request, pk):
	item = Task.objects.get(id=pk)

	if request.method == 'POST':
		item.delete()
		return redirect('/index')

	context = {
		'item':item,
		}
	return render(request, 'delete.html', context)

@login_required(login_url='login')
def categories(request):
	category = Category.objects.all()

	print('Majid Jordan')

	# categoryForm = CategoryForm(instance=task)

	if request.method == 'POST':
		print('Majid Jordan1')

		categoryForm = CategoryForm(request.POST)
		
		if categoryForm.is_valid():
			categoryForm.save()
		print('Majid Jordan 3')
		return redirect('/')

	context = {'category': category}
	return render(request, 'categories.html', context)

def profile(request):
	users = Kin.objects.all()

	context = {'users':users}
	return render(request, 'profile.html', context)

def add_user(request):
	users = Kin.objects.all()
	form = ProfileForm()

	if request.method == 'POST':
		form = ProfileForm(request.POST)
		if form.is_valid:
			print('Form is valid')
			form.save()
		else:
			print(form.errors)
			print('Could not process')
			return('profile.html')

	context = {'users':users, 'form':form}
	return render(request, 'add_user.html', context)