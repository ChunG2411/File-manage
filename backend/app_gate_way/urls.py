from django.urls import path

from app_user.views import (
    RegisterUser, LoginView, LogoutView,
    MyProfileView, ProfileView, RequestView,
    LimitView,
    EmailView
)
from app_file.views import(
    HomeView,
    FolderView, FolderDetailView,
    FileView, downloadFile
)


urlpatterns = [
    path('register', RegisterUser.as_view(), name="RegisterUser"),
    path('login', LoginView.as_view(), name="LoginView"),
    path('logout', LogoutView.as_view(), name="LogoutView"),

    path('my-profile', MyProfileView.as_view(), name="MyProfileView"),
    path('profile/<str:username>', ProfileView, name="ProfileView"),

    path('request', RequestView.as_view(), name="RequestView"),
    path('request/<str:id>', RequestView.as_view(), name="RequestView-action"),
    path('limit', LimitView.as_view(), name="LimitView"),

    path('email', EmailView.as_view(), name="EmailView"),

    path('home', HomeView, name="HomeView"),
    path('folder', FolderView.as_view(), name="FolderView-add"),
    path('folder/<str:id>', FolderView.as_view(), name="FolderView"),
    path('folder/<str:id>/detail', FolderDetailView.as_view(), name="FolderDetailView"),

    path('file', FileView.as_view(), name="FileView-add"),
    path('file/<str:id>', FileView.as_view(), name="FileView"),
    path('file/<str:id>/detail', FileView.as_view(), name="FileDetailView"),
    path('file/<str:id>/download', downloadFile, name="downloadFile"),
]
