from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('index/', views.index, name='index'),
    path('chemical/', views.chemical_lab, name='chemical_lab'),
    path('chemical_reaction_view', views.chemical_reaction_view, name='reaction'),
]