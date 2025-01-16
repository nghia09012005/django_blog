from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('project/', views.project, name='project'),
    path('contactme/', views.contactme, name='contactme'),
    path('search/',views.search_videos, name='search_videos'),
    path('result/',views.result,name='result'),
    path('',views.login,name='login')
]