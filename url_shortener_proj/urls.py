"""url_shortener_proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import login, logout

from short_app import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.IndexView.as_view(), name='index_view'),
    url(r'^signup/$', views.SignUpView.as_view(), name='sign_up_view'),
    url(r'^login/$', login, name='login_view'),     # https://docs.djangoproject.com/en/1.9/topics/auth/default/#how-to-log-a-user-in
    url(r'^logout/$', logout, {'next_page': 'index_view'}, name='logout_view'),
    url(r'^all_bookmarks/$', views.BookmarkView.as_view(), name='bookmark_view'),
    url(r'^accounts/profile/$', views.ProfileView.as_view(), name='profile_view'),
    url(r'^accounts/profile/hist/(?P<pk>\d+)$', views.ClickView.as_view(), name='click_view'),
    url(r'^accounts/profile/edit_link/(?P<pk>\d+)/$', views.EditBookmark.as_view(), name='edit_bookmark_view'),
    url(r'^accounts/profile/edit_link/(?P<pk>\d+)/delete/$', views.LinkDelete.as_view(), name='delete_bookmark_view'),
    url(r'^shorten_link/$', views.ShortenLink.as_view(), name='shorten_link'),
    url(r'^d/(?P<hash_id>\w+)', views.ForwardView.as_view(), name='forward_view'),     # http://ccbv.co.uk/projects/Django/1.9/django.views.generic.base/RedirectView/

]
