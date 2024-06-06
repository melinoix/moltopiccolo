from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('quiz/', views.quiz,name='quiz'),
    path('time_up/', views.time_up, name='time_up'),
    
]
