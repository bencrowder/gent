from django.contrib import admin
from gent.models import Tag, Target, Item

class TargetAdmin(admin.ModelAdmin):
    list_display = ('husband_name', 'husband_id', 'wife_name', 'wife_id', 'date_created')

class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'completed', 'date_created', 'date_completed', 'order')

admin.site.register(Tag)
admin.site.register(Target, TargetAdmin)
admin.site.register(Item, ItemAdmin)
