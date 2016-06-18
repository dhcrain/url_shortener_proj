from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, RedirectView, UpdateView, ListView, DeleteView
from hashids import Hashids

from short_app.models import Bookmark, Click


class IndexView(TemplateView):
    template_name = 'index.html'


class SignUpView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = '/login/'


# @login_required()
class ProfileView(ListView):        # ListView ?
    template_name = 'profile.html'
    model = Bookmark


class ShortenLink(CreateView):
    model = Bookmark
    fields = ['title', 'description', 'url']
    success_url = 'accounts/profile/'

    def form_valid(self, form):
        hashids = Hashids(salt="yabbadabbadooo")
        bookmark = form.save(commit=False)
        bookmark.user = self.request.user
        bookmark.hash_id = hashids.encode(id(bookmark.url))
        return super(ShortenLink, self).form_valid(form)


class ForwardView(RedirectView):

    # record click and incriment the count on the Bookmark table

    def get(self, request, *args, **kwargs):
        hash_id = self.kwargs.get('hash_id', None)      # gets hash_id
        link = Bookmark.objects.get(hash_id=hash_id)    # looks up the link from the hash_id
        self.url = '{}'.format(link.url)
        return super(ForwardView, self).get(request, args, **kwargs)


class EditBookmark(UpdateView):
    model = Bookmark
    fields = ['title', 'description', 'url']
    success_url = '/accounts/profile/'
    template_name = 'update.html'


class LinkDelete(DeleteView):
    model = Bookmark
    success_url = '/accounts/profile/'

    def get_object(self, queryset=None):
        link = super(LinkDelete, self).get_object()
        if not link.user == self.request.user:
            raise Http404
        hashid = Bookmark.objects.get(id=link.id)
        self.hashid = hashid
        return link

    # def get_success_url(self):
    #     return reverse('/profile/')        # error here
