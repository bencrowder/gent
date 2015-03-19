from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=250)
    owner = models.ForeignKey(User)

    def __unicode__(self):
        return self.name


class Family(models.Model):
    husband_name = models.CharField('Husband: Name', max_length=250, blank=True)
    husband_id = models.CharField('Husband: FamilyTree ID', max_length=50, blank=True)
    wife_name = models.CharField('Wife: Name', max_length=250, blank=True)
    wife_id = models.CharField('Wife: FamilyTree ID', max_length=50, blank=True)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name='families', blank=True, null=True)
    owner = models.ForeignKey(User)
    starred = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "families"

    def __unicode__(self):
        return ' / '.join([self.husband_name, self.wife_name])

    def html(self):
        return ' <span>/</span> '.join([self.husband_name, self.wife_name])

    # Return incomplete items
    def incomplete_items(self):
        return self.items.filter(completed=False).order_by('order')

    # Return latest incomplete items
    def latest_incomplete_items(self):
        return self.items.filter(completed=False).order_by('-date_created')

    # Return incomplete items label
    def incomplete_items_label(self):
        num_items = len(self.incomplete_items())

        return '{} item{}'.format(num_items, 's' if num_items != 1 else '')

    # Return completed items
    def completed_items(self):
        return self.items.filter(completed=True).order_by('-date_completed')


class Item(models.Model):
    title = models.CharField(max_length=500)
    family = models.ForeignKey(Family, related_name='items')

    completed = models.BooleanField(default=False)
    date_completed = models.DateTimeField(blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name='items', blank=True, null=True)
    order = models.IntegerField(default=0)
    notes = models.TextField(blank=True)
    owner = models.ForeignKey(User)
    starred = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title
