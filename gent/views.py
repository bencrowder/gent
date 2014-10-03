from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, QueryDict
from django.db.models import Q, Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Tag, Target, Item

#@login_required()
def home(request):
    # Get list of tags
    tags = Tag.objects.all().annotate(num_items=Count('items')).order_by('-num_items', 'name')[:10]

    # Get list of recent targets (targets with most recent items)
    # Go through extra stuff to make it unique
    items = Item.objects.all().order_by('-date_created')[:30]
    targets = set()
    targets_add = targets.add
    recent_targets = [i.target for i in items if not (i.target in targets or targets_add(i.target))]

    # Get list of recent items
    recent_items = Item.objects.all().order_by('-date_created')[:3]

    # Get list of targets with most todos
    # TODO: use # incomplete items instead
    largest_targets = Target.objects.all().annotate(num_items=Count('items')).order_by('-num_items')[:3]

    return render(request, 'home.html', {'user': request.user, 'title': 'Gent', 'tags': tags, 'recent_targets': recent_targets, 'recent_items': recent_items, 'largest_targets': largest_targets})

#@login_required()
def search(request):
    query = request.GET.get('q', '')

    # Search by item title, item notes, target names, target FT IDs, target notes, or tag
    # Returns items and targets that match
    # TODO: replace with Whoosh

    target_list = []
    item_list = []
    tag_list = []

    if query:
        if query[0:4] == 'tag:':
            # Special case for tag searching
            tag = query[4:]

            target_list = Target.objects.filter(tags__name=tag).distinct().order_by('husband_name', 'wife_name')

            item_list = Item.objects.filter(tags__name=tag).order_by('title')
        else:
            # Get targets that match
            target_list = Target.objects.filter(
                Q(husband_name__icontains=query)
                | Q(husband_id__icontains=query)
                | Q(wife_name__icontains=query)
                | Q(wife_id__icontains=query)
                | Q(notes__icontains=query)
            ).distinct().order_by('husband_name', 'wife_name')

            # Get items that match
            item_list = Item.objects.filter(
                Q(title__icontains=query)
                | Q(notes__icontains=query)
            ).distinct().order_by('order')

            # Get tags that match
            tag_list = Tag.objects.filter(
                Q(name__icontains=query)
            ).distinct().order_by('name')

    return render(request, 'search.html', {'user': request.user, 'title': '{} - Gent'.format(query), 'targets': target_list, 'items': item_list, 'tags': tag_list, 'query': query})

#@login_required()
def target(request, target_id):
    # Get target
    target = Target.objects.get(id=target_id)

    return render(request, 'target.html', {'user': request.user, 'title': '{} - Gent'.format(target),'target': target})

def logout(request):
    return logout_then_login(request)
