from django.conf import settings
from django.conf.urls import include, url, patterns
from django.conf.urls.static import static
from django.contrib import admin
from ajax_select import urls as ajax_select_urls


urlpatterns = [
    # Examples:
    url(r'^$', 'newsletter.views.home', name='home'),
    url(r'^contact/$', 'newsletter.views.contact', name='contact'),
    url(r'^profile/$', 'newsletter.views.profile', name='profile'),
    url(r'^officeView/$', 'newsletter.views.officeView', name='officeView'),
    url(r'^officeView/(?P<slug>[\w.@+-]+)$', 'newsletter.views.officeView', name='officeView'),
    url(r'^officeCreate/$', 'newsletter.views.officeCreate', name='officeCreate'),
    url(r'^search/$', 'newsletter.views.searchView', name='search'),
    url(r'^war_list/$', 'newsletter.views.war_list', name='war_list'),
    url(r'^create/$', 'newsletter.views.war_main', name='create'),
    url(r'^create2/$', 'newsletter.views.create', name='create'),
    url(r'^war_edit/$', 'newsletter.views.war_main', name='war_edit'),
    url(r'^sort/$', 'newsletter.views.sort', name='sort'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^war_view/$', 'newsletter.views.war_view', name='war_view'),
    url(r'^war_playerview/(?P<war_name>[\w.@+-]+)', 'newsletter.views.war_view', name='war_playerview'),
    url(r'^war_view/(?P<war_name>[\w.@+-]+)/(?P<user>[\w.@+-]+)/(?P<vote>[\w.@+-]+)', 'newsletter.views.war_view', name='war_like'),
    url(r'^war_view/(?P<war_name>[\w.@+-]+)/(?P<user>[\w.@+-]+)/(?P<loss>[\w.@+-]+)', 'newsletter.views.war_view',
        name='war_loss'),
    url(r'^ajax_select/', include(ajax_select_urls)),
    url(r'^tinymce/', include('tinymce.urls')),


    # url(r'^error/$', 'newsletter.views.sort', name='error'),


]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += patterns('',
                            url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                                'document_root': settings.MEDIA_ROOT,
                            }))

