from django.urls import path
from .views import UserRegisterView, UserEditView,  PasswordsChangeView, ProfilePageView, EditProfilePageView, CreateProfilePageView
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('edit_profile/', UserEditView.as_view(), name='edit_profile'),
    # path('password/', auth_views.PasswordChangeView.as_view(template_name='registration/change-password.html')),
    path('password/', PasswordsChangeView.as_view(template_name='registration/change-password.html')),
    path('password_updated', views.password_updated, name='password_updated'),
    path('<int:pk>/profile/', ProfilePageView.as_view(), name='profile_page'),
    path('<int:pk>/edit_profile/', EditProfilePageView.as_view(), name='edit_profile_page'),
    path('create_profile_page/', CreateProfilePageView.as_view(), name='create_profile_page'),
]


