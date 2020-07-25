from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic import DetailView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .forms import SignUpForm, EditProfileForm, PasswordUpdateForm
from blog.models import Profile


class EditProfilePageView(generic.UpdateView):
    model = Profile
    template_name = 'registration/edit_profile_page.html'
    fields = ['profile_pic', 'website_url', 'facebook_url', 'twitter_url', 'instagram_url', 'whatsapp_url', 'bio']
    success_url = reverse_lazy('blog-home')



class ProfilePageView(DetailView):
    model = Profile
    template_name = 'registration/user_profile.html'

    def get_context_data(self, *args, **kwargs):
        # users = Profile.objects.all()
        context = super(ProfilePageView, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(Profile, id = self.kwargs['pk'])
        context["page_user"] = page_user
        return context


class PasswordsChangeView(PasswordChangeView):
    # form_class = PasswordUpdateForm
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_updated')
    # success_url = reverse_lazy('blog-home')


def password_updated(request):
    return render(request, 'registration/password_updated.html', {})


class UserRegisterView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


class UserEditView(generic.UpdateView):
    form_class = EditProfileForm
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('blog-home')


    def get_object(self):
        return self.request.user
# Create your views here.
