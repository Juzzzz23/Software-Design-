from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('landing/<str:username>/', views.landing, name='landing'),
    path('welcome/<str:username>/', views.welcome, name='welcome'),
    path('planner/', views.planner, name='planner'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile')

]
