from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Target(models.Model):
    husband_name = models.CharField('Husband: Name', max_length=250, blank=True)
    husband_id = models.CharField('Husband: FamilyTree ID', max_length=50, blank=True)
    wife_name = models.CharField('Wife: Name', max_length=250, blank=True)
    wife_id = models.CharField('Wife: FamilyTree ID', max_length=50, blank=True)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    tags = models.ForeignKey(Tag, related_name='targets', blank=True, null=True)

    def __str__(self):
        return ' & '.join([self.husband_name, self.wife_name])

    # Return incomplete items
    def incomplete_items(self):
        return self.items.filter(completed=False)

    # Return completed items
    def completed_items(self):
        return self.items.filter(completed=True)


class Item(models.Model):
    title = models.CharField(max_length=500)
    target = models.ForeignKey(Target, related_name='items')

    completed = models.BooleanField(default=False)
    date_completed = models.DateTimeField(blank=True, null=True)

    date_created = models.DateTimeField(auto_now_add=True)
    tags = models.ForeignKey(Tag, related_name='items', blank=True, null=True)
    order = models.IntegerField(default=0)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.title
