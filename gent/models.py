from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=250)


class Target(models.Model):
    name = models.CharField(max_length=250)
    ft_id = models.CharField(max_length=50, blank=True)
    name2 = models.CharField(max_length=250)
    ft_id2 = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    tags = models.ForeignKey(Tag, related_name='targets')

    def __str__(self):
        response = self.name
        if self.name2:
            response += ' / {}'.format(self.name2)
        return response


class Item(models.Model):
    title = models.CharField(max_length=500)
    completed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField('date completed')
    tags = models.ForeignKey(Tag, related_name='items')
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title
