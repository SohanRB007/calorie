from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum

from .forms import RegisterForm, ProfileForm, DailyCalorieForm
from .models import Profile, DailyCalorie
def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        login(request, user)
        return redirect('profile')
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'login.html')



@login_required
def profile_view(request):
    form = ProfileForm(request.POST or None)
    if form.is_valid():
        profile = form.save(commit=False)
        profile.user = request.user
        profile.save()
        return redirect('dashboard')
    return render(request, 'profile.html', {'form': form})


@login_required
def dashboard_view(request):
    profile = Profile.objects.get(user=request.user)

    if profile.gender == "Male":
        required_calories = 66.47 + (13.75 * profile.weight) + (5.003 * profile.height) - (6.755 * profile.age)
    else:
        required_calories = 655.1 + (9.563 * profile.weight) + (1.850 * profile.height) - (4.676 * profile.age)

    today = timezone.localdate()
    today_total = (DailyCalorie.objects
                   .filter(user=request.user, date=today)
                   .aggregate(Sum('calorie_consumed'))['calorie_consumed__sum'] or 0)

    return render(request, 'dashboard.html', {
        'required_calories': required_calories,
        'today_total': today_total,
    })

@login_required
def calories_list(request):
    items = DailyCalorie.objects.filter(user=request.user).order_by('-date', '-id')
    total = items.aggregate(Sum('calorie_consumed'))['calorie_consumed__sum'] or 0
    return render(request, 'calories_list.html', {'items': items, 'total': total})


@login_required
def calories_add(request):
    form = DailyCalorieForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        return redirect('calories_list')
    return render(request, 'calories_add.html', {'form': form})


@login_required
def calories_edit(request, pk):
    item = get_object_or_404(DailyCalorie, pk=pk, user=request.user)
    form = DailyCalorieForm(request.POST or None, instance=item)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('calories_list')
    return render(request, 'calories_edit.html', {'form': form, 'item': item})


@login_required
def calories_delete(request, pk):
    item = get_object_or_404(DailyCalorie, pk=pk, user=request.user)
    if request.method == "POST":
        item.delete()
        return redirect('calories_list')
    return render(request, 'calories_delete.html', {'item': item})