from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'', include('player.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tournaments/', include('player.urls')),
    # Examples:
    # url(r'^$', 'touchdb.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
)
