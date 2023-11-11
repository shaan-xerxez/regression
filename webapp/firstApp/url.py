from django.contrib import admin
from django.urls import path, include
from firstApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index, name='index'),
    path('result/', views.result, name='result'),
    path('', views.SignupPage, name='signup'),
    path('login/', views.LoginPage, name='login'),
    path('logout/', views.LogoutPage, name='logout'),    
]
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('index/', views.index, name='index'),
#     path('result/', views.result, name='result'),  # Change the URL pattern to 'result'
#     path('signup/', views.SignupPage, name='signup'),  # Change the URL pattern to 'signup'
#     path('login/', views.LoginPage, name='login'),
#     path('logout/', views.LogoutPage, name='logout'),
# ]