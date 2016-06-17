from django.contrib import admin

# Register your models here.

from short_app.models import Click, Bookmark

admin.site.register(Bookmark)
admin.site.register(Click)
