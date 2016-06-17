from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from hashids import Hashids

from short_app.models import Bookmark


class IndexView(TemplateView):
    template_name = 'index.html'


class SignUpView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = '/'


class ProfileView(TemplateView):        # ListView ?
    template_name = 'profile.html'


class ShortenLink(CreateView):
    model = Bookmark
    fields = ['title', 'description', 'url', 'hash_id', 'count']
    success_url = 'ProfileView'

