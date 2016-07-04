from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'', include('player.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('player.urls')),
    # Examples:
    # url(r'^$', 'restdjango.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
)
