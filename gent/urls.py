from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'gent.views.home', name='home'),
    url(r'^search/$', 'gent.views.search', name='search'),
    url(r'^target/(?P<target_id>.+?)/$', 'gent.views.target', name='target'),
    url(r'^item/(?P<item_id>.+?)/$', 'gent.views.item', name='item'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^logout/$', 'gent.views.logout', name='logout'),

    url(r'^ws/target/update-item-order/$', 'gent.views.ws_update_item_order', name='update_item_order'),
    url(r'^ws/item/toggle-complete/$', 'gent.views.ws_toggle_item_complete', name='toggle_item_complete'),
)
