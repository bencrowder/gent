from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'gent.views.home', name='home'),
    url(r'^search/$', 'gent.views.search', name='search'),
    url(r'^family/(?P<family_id>.+?)/$', 'gent.views.family', name='family'),
    url(r'^item/(?P<item_id>.+?)/$', 'gent.views.item', name='item'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),

    url(r'^ws/family/update-item-order/$', 'gent.views.ws_update_item_order', name='ws_update_item_order'),
    url(r'^ws/family/search/$', 'gent.views.ws_family_search', name='ws_family_search'),
    url(r'^ws/family/$', 'gent.views.ws_family', name='ws_family'),

    url(r'^ws/item/toggle-complete/$', 'gent.views.ws_toggle_item_complete', name='ws_toggle_item_complete'),
    url(r'^ws/item/$', 'gent.views.ws_item', name='ws_item'),
)
