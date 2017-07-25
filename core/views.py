from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout

# User Auth based on CBV
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView

# User Model Built-in Django
from django.contrib.auth.models import User

from django.views import generic
from django.views.generic import TemplateView

# External Models
from posts.models import Post

# Forms
from .forms import SignUpForm, LoginForm

class IndexTemplateView(generic.TemplateView):
    """
    Index shows posts, last users.
    """
    model = Post
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexTemplateView, self).get_context_data(**kwargs)
        context['posts'] = Post.objects.all()[:5]
        context['users'] = User.objects.all()[:5]
        return context

# Signup https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html#sign-up-with-profile-model
def signup(request):
    if request.user.is_authenticated():
        return redirect('timeline')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.userprofile.bio = form.cleaned_data.get('bio')
            user.userprofile.website = form.cleaned_data.get('website')
            user.userprofile.location = form.cleaned_data.get('location')
            user.userprofile.date_birth = form.cleaned_data.get('date_birth')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('timeline')
    else:
        form = SignUpForm()
    return render(request, 'core/signup.html', {'form': form})

class UserLogout(LogoutView):
    next_page = 'login'
    redirect_field_name = 'next'

class UserLogin(LoginView):
    success_url = 'timeline'
    form_class = LoginForm