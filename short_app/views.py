from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, RedirectView
from hashids import Hashids

from short_app.models import Bookmark, Click


class IndexView(TemplateView):
    template_name = 'index.html'


class SignUpView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = '/'


# @login_required()
class ProfileView(TemplateView):        # ListView ?
    template_name = 'profile.html'


class ShortenLink(CreateView):
    model = Bookmark
    fields = ['title', 'description', 'url']
    success_url = 'hashed_link'
    # print(Bookmark.objects.get(id)

    def form_valid(self, form):
        hashids = Hashids(salt="yabbadabbadooo")
        bookmark = form.save(commit=False)
        bookmark.user = self.request.user
        bookmark.hash_id = hashids.encode(id(bookmark.url))
        return super(ShortenLink, self).form_valid(form)


class HashedLink(TemplateView):
    template_name = 'hashed_link.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["hash"] = Hash.objects.all()
        return context


class ForwardView(RedirectView):

    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        short_url = kwargs["short_url"]
        return Bookmark.expand(short_url)
