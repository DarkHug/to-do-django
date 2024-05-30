from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('all-task', views.show_task, name='all_task'),
    path('add-task/', views.add_task, name='add_task'),
    path('edit-task/<int:id>', views.edit_task, name='edit_task'),
    path('delete-task/<int:id>', views.delete_task, name='delete_task'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
]
