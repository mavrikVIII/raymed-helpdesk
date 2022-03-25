from django.urls import path
from . import views
from django.contrib.auth import views as standart_views

app_name = "registration"

urlpatterns = [
    path('index', views.index, name = 'index'),
    path('', views.home, name = 'home'),
    # path('home', views.home, name = 'home'),
    path('login', standart_views.LoginView.as_view(), name='login'),
    path('logout/', standart_views.LogoutView.as_view(), name='logout'),
    # path('register/', views.register, name = 'register'),
    #


]
