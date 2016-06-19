import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.dispatch import receiver
from django.http import HttpResponseRedirect, Http404, request
from django.views.generic import TemplateView, CreateView, RedirectView, UpdateView, ListView, DeleteView
from django.views.generic.list import MultipleObjectMixin
from hashids import Hashids
from short_app.models import Bookmark, Click


class IndexView(ListView):
    model = Bookmark
    template_name = 'index.html'
    paginate_by = 3


class SignUpView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = '/login/'


class ProfileView(ListView):
    template_name = 'profile.html'
    model = Bookmark

    def get_context_data(self, **kwargs):
        # user_id = self.kwargs.get('user', None)  # gets Bookmark PK
        context = super().get_context_data(**kwargs)  # I have no idea what this does
        if self.request.user.is_authenticated():
            context["bookmark"] = Bookmark.objects.filter(user_id=self.request.user)
        else:
            context["bookmark"] = Bookmark.objects.all()
        return context


class ShortenLink(CreateView):
    model = Bookmark
    fields = ['title', 'url', 'description']
    success_url = '/accounts/profile/'

    def form_valid(self, form):
        hashids = Hashids(salt="yabbadabbadooo")
        bookmark = form.save(commit=False)
        bookmark.hash_id = hashids.encode(id(bookmark.url))
        # allows unregisted users to shorten a link, assigned to 'webuser' id=6, this seems a little hacky
        if self.request.user.is_authenticated():
            bookmark.user = self.request.user
        else:
            bookmark.user = User.objects.get(id=6)
        return super(ShortenLink, self).form_valid(form)


class ForwardView(RedirectView):

    # https://godjango.com/15-class-based-views-part-1-templateview-and-redirectview/
    def get(self, request, *args, **kwargs):
        hash_id = self.kwargs.get('hash_id', None)      # gets hash_id
        link = Bookmark.objects.get(hash_id=hash_id)    # looks up the link from the hash_id
        self.url = link.url
        link.count += 1         # increment the count on the Bookmark table
        link.save()
        Click.objects.create(link=link, time_click=datetime.datetime.now())
        return super(ForwardView, self).get(request, args, **kwargs)


class EditBookmark(LoginRequiredMixin, UpdateView):
    model = Bookmark
    fields = ['title', 'description', 'url']
    success_url = '/accounts/profile/'
    template_name = 'update.html'


class LinkDelete(LoginRequiredMixin, DeleteView):
    model = Bookmark
    success_url = '/accounts/profile/'

    def get_object(self, queryset=None):
        link = super(LinkDelete, self).get_object()
        if not link.user == self.request.user:
            raise Http404
        hashid = Bookmark.objects.get(id=link.id)
        self.hashid = hashid
        return link


class ClickView(TemplateView):
    model = Click
    template_name = "short_app/click_list.html"

    def get_context_data(self, **kwargs):
        bookmark_pk = self.kwargs.get('pk', None)      # gets Bookmark PK
        context = super().get_context_data(**kwargs)    # I have no idea what this does
        context["bookmark"] = Bookmark.objects.get(id=bookmark_pk)
        context["clicks"] = Click.objects.filter(link=bookmark_pk)
        return context


class BookmarkView(ListView):
    model = Bookmark


class UserView(ListView):
    model = User

