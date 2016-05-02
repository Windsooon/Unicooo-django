from django.shortcuts import render
from .form import UserCreateForm, UserLoginForm
from django.contrib.auth import get_user_model
from .models import CustomAuth
from django.contrib.auth import authenticate, login as django_login

def front_page(request):
    return render(request, "frontpage.html")

def public_activities(request):
    return render(request, "public_activities.html")

def sign_up(request):
    if request.method == 'GET':
        form = UserCreateForm()
        return render(request, "signup.html", {"form": form})
    elif request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['user_name']
            email = form.cleaned_data['email']
            password = form.clean_password2()
            User = get_user_model()
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            user_id = user.id
            if request.POST.get("first", None):
                try:
                    token =  Token.objects.get(user_id=user_id).key
                except DoesNotExist:
                    return HttpResponse(status=405)
            return redirect('common/frontpage')
        else:
            return render(request, '404.html')
    else:
        return render(request, '404.html')

def login_in(request):
    if request.method == 'GET':
        form = UserLoginForm()
        return render(request, "login.html", {"form": form})
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email', None)
            password = request.POST.get('password', None)
            user = authenticate(email=email, password=password)
            if user is not None:
                if user.is_active:
                    django_login(request, user)
                    return redirect("/")
            else:
                return render(request, '404.html')
        else:
            return render(request, '404.html')
    elif request.method == 'GET':
        form = UserLoginForm()
        return render(request, 'login.html', {"form": form})
    else:
        return render(request, '404.html')

    

