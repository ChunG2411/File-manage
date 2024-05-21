from django.urls import path

from app_user.views import (
    RegisterUser, TokenView, LogoutView, GetCode,
    MyProfileView, ProfileView, RequestView,
    LimitView,
    EmailView
)
from app_file.views import(
    HomeView, SearchView,
    FolderView, FolderDetailView,
    FileView, FileDetailView, downloadFile, previewFile
)


urlpatterns = [
    path('register', RegisterUser.as_view(), name="RegisterUser"),
    path('login', TokenView.as_view(), name="TokenView"),
    path('logout', LogoutView.as_view(), name="LogoutView"),

    path('get-code', GetCode.as_view(), name="GetCode"),
    path('my-profile', MyProfileView.as_view(), name="MyProfileView"),
    path('profile/<str:username>', ProfileView.as_view(), name="ProfileView"),
    path('profile/<str:username>/delete', ProfileView.as_view(), name="ProfileView-delete"),

    path('request', RequestView.as_view(), name="RequestView"),
    path('request/<str:id>', RequestView.as_view(), name="RequestView-action"),
    path('limit', LimitView.as_view(), name="LimitView"),

    path('email', EmailView.as_view(), name="EmailView"),

    path('home', HomeView.as_view(), name="HomeView"),
    path('search', SearchView.as_view(), name="SearchView"),

    path('folder', FolderView.as_view(), name="FolderView-add"),
    path('folder/<str:id>', FolderView.as_view(), name="FolderView"),
    path('folder/<str:id>/detail', FolderDetailView.as_view(), name="FolderDetailView"),

    path('file', FileView.as_view(), name="FileView-add"),
    path('file/<str:id>', FileView.as_view(), name="FileView"),
    path('file/<str:id>/detail', FileDetailView.as_view(), name="FileDetailView"),
    path('file/<str:id>/download', downloadFile, name="downloadFile"),
    path('file/<str:id>/preview', previewFile, name="previewFile"),
]
