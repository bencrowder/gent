from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'gent.views.home', name='home'),
    url(r'^search/$', 'gent.views.search', name='search'),
    url(r'^target/(?P<target_id>.+?)/$', 'gent.views.target', name='target'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^logout/$', 'gent.views.logout', name='logout'),

    url(r'^ws/target/update-item-order/$', 'gent.views.ws_update_item_order', name='update_item_order'),
)
