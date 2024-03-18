from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginForm, name = "userLogin"),
    path('logout/', views.logoutUser, name = "userLogout"),
    path('delete-msg/<str:pk>', views.deleteMessage, name = "deleteMessage"),
    #path('edit-msg/<str:pk>', views.editMessage, name = "edit-msg"),
    path('user/<str:pk>', views.userPage, name = "user_profile"),
    path('register/', views.registerUser, name = "registerUser"),
    path('', views.home, name = "home"),
    path('group/<str:pk>/', views.group, name = "group"),
    path('create_group/', views.create_group, name = "create_group"),
    path('edit-group/<str:pk>/', views.edit_group, name = "edit_group"),
    path('delete_grp/<str:pk>/', views.deleteGroup, name = "del_grp"),
    path('edit-user', views.editUser, name = "edit-user")
]