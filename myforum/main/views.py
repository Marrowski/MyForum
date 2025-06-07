from django.shortcuts import render
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .models import UserProfile
from .forms import ChangeProfileForm

def main_view(request):
    forum = ForumPage.objects.all()
    user = request.user
    user_data = User.objects.filter(username=user)

    
    context = {
        'forum': forum,
        'user': user_data
    }
    
    return render(request, 'main/main.html', context)


def post_page(request, post_id):
    post = get_object_or_404(ForumPage, id=post_id)
    user = request.user
    user_data = User.objects.filter(username=user)
    
    context = {
        'post': post,
        'user': user_data
    }
    
    return render(request, 'main/post_page.html', context)


def games_view(request):
    forum = ForumPage.objects.filter(forum_choise='І')
    user = request.user
    user_data = User.objects.filter(username=user)
    
    context = {
        'forum': forum,
        'user': user_data
    }
    
    return render(request, 'main/games.html', context)


def computers_view(request):
    forum = ForumPage.objects.filter(forum_choise='К')
    user = request.user
    user_data = User.objects.filter(username=user)
    
    context = {
        'forum': forum,
        'user': user_data
    }
    
    return render(request, 'main/computers.html', context)


def programming_view(request):
    forum = ForumPage.objects.filter(forum_choise='П')
    user = request.user
    user_data = User.objects.filter(username=user)
    
    context = {
        'forum': forum,
        'user': user_data
    }
    
    return render(request, 'main/programming.html', context)


def news_view(request):
    forum = ForumPage.objects.filter(forum_choise='Н')
    user = request.user
    user_data = User.objects.filter(username=user)
    
    context = {
        'forum': forum,
        'user': user_data
    }
    
    return render(request, 'main/news.html', context)


def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if not username or not password or not password2:
            messages.error(request, 'Будь ласка, заповність всі поля')
            return render(request, 'main/register.html')
        
        if password != password2:
            messages.error(request, 'Паролі не співпадають. Спробуйте ще раз')
            return render(request, 'main/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Такий користувач вже існує.')
            return render(request, 'main/register.html')
        
        user = User.objects.create_user(email=email, username=username, password=password)
        user.save()
        
        login(request, user)
        
        return redirect('main')
    
    return render(request, 'main/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            try:
                profile = user.profile
            except UserProfile.DoesNotExist:
                profile = UserProfile.objects.create(user=user)

            return redirect('main')
        else:
            messages.error(request, 'Ім`я користувача або пароль не правильні.')
            
    return render(request, 'main/login.html')



@login_required
def logout_view(request):
    logout(request)
    return redirect('main')


@login_required
def user_profile(request):
    profile = UserProfile.objects.get(user=request.user)
    context = {
        'profile': profile,
    }
    return render(request, 'main/profile.html', context)


@login_required
def profile_settings(request):
    username = request.POST.get('username')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')     
    
    user = request.user
    profile = user.profile
    updated = False
        
    if request.method == 'POST': 
        form = ChangeProfileForm(request.POST, request.FILES, instance=profile)

        if username:
            if username and username != user.username:
                if User.objects.filter(username=username).exclude(pk=user.pk).exists():
                    messages.error(request, 'Такий користувач вже існує.')
                    return render(request, 'main/profile_settings.html')
                else:
                    user.username = username
                    user.save()
                    updated = True
                    messages.success(request, 'Ім`я користувача успішно змінено.')
        else:
            messages.error(request, 'Нікнейм не може бути пустим')
        
        
        if password1 or password2:
            if not password1 or not password2:
                messages.error(request, 'Поля з паролями повинні бути заповнені.')
                return render(request, 'main/profile_settings.html')
            if password1 != password2:
                messages.error(request, 'Паролі не співпадають.')
                return render(request, 'main/profile_settings.html')
            else:
                user.set_password(password1)
                update_session_auth_hash(request, user)
                user.save()
                updated = True
                messages.success(request, 'Пароль успішно змінено.')
        
        if form.is_valid():
            form.save()
            img_obj = form.instance
            
            messages.success(request, 'Зображення профілю успішно оновлено.')
        else:
            messages.error(request, 'Помилка при завантаженні зображення.')
        
        if not updated and not form.changed_data:
            messages.info(request, 'Нічого не змінено.')
            
        return render(request, 'main/profile_settings.html', {'form': form, 'img_obj':img_obj})
    
    form = ChangeProfileForm(instance=profile)             
    return render(request, 'main/profile_settings.html', {'form': form})

            
            
    
        