from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Daily calories CRUD
    path('calories/', views.calories_list, name='calories_list'),
    path('calories/add/', views.calories_add, name='calories_add'),
    path('calories/<int:pk>/edit/', views.calories_edit, name='calories_edit'),
    path('calories/<int:pk>/delete/', views.calories_delete, name='calories_delete'),
]