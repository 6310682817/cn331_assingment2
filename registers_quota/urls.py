from django.urls import path

from . import views

urlpatterns = [
    # index page
    path("", views.index, name="index"),
    path("index/", views.index, name="index"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # student user
    path('search/', views.search, name='search'),
    path('quota/', views.quota, name='quota'),
    path('status/', views.status, name='status'),
   
    # admin user
    path('admin_search/', views.admin_search, name='admin_search'),
    path('student/', views.student, name='student'),
    path('checkStu/', views.checkStu, name='checkStu'),
    path('checkSub/', views.checkSub, name='checkSub'),
]