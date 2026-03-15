from django.urls import path
from .views import Dashboard, RegisterView, LogoutUser, ProfileView, ProfileUpdateView,ChangePasswordView
from django.contrib.auth.views import LoginView

urlpatterns = [
    path("", Dashboard.as_view(), name="home"),
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutUser.as_view(), name="logout"),
    path("signup/", RegisterView.as_view(), name="signup"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile-update/", ProfileUpdateView.as_view(), name="profile_edit"),
    path("profile/change-password/", ChangePasswordView.as_view(), name="change_password"),
]