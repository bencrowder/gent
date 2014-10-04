from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, QueryDict
from django.db.models import Q, Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Tag, Family, Item
import datetime

@login_required()
def home(request):
    # Get list of tags
    tags = Tag.objects.all().annotate(num_items=Count('items')).order_by('-num_items', 'name')[:10]

    # Get list of recent families (families with most recent items)
    # Go through extra stuff to make it unique
    items = Item.objects.all().order_by('-date_created')[:30]
    families = set()
    families_add = families.add
    recent_families = [i.family for i in items if not (i.family in families or families_add(i.family))]
    recent_families = recent_families[:3]

    # Get list of recent items
    recent_items = Item.objects.filter(completed=False).order_by('-date_created')[:3]

    # Get list of families with most todos
    # TODO: use # incomplete items instead
    top_families = Family.objects.all().annotate(num_items=Count('items')).order_by('-num_items')[:3]

    return render(request, 'home.html', {'user': request.user, 'title': 'Gent', 'tags': tags, 'recent_families': recent_families, 'recent_items': recent_items, 'top_families': top_families})

@login_required()
def search(request):
    query = request.GET.get('q', '')

    # Search by item title, item notes, family names, family FT IDs, family notes, or tag
    # Returns items and families that match
    # TODO: replace with Whoosh

    family_list = []
    item_list = []
    tag_list = []

    if query:
        if query[0:4] == 'tag:':
            # Special case for tag searching
            tag = query[4:]

            family_list = Family.objects.filter(tags__name=tag).distinct().order_by('husband_name', 'wife_name')

            item_list = Item.objects.filter(tags__name=tag).order_by('title')
        else:
            # Get families that match
            family_list = Family.objects.filter(
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

    return render(request, 'search.html', {'user': request.user, 'title': '{} - Gent'.format(query), 'families': family_list, 'items': item_list, 'tags': tag_list, 'query': query})

@login_required()
def family(request, family_id):
    # Get family
    try:
        family = Family.objects.get(id=family_id)

        if family:
            return render(request, 'family.html', {'user': request.user, 'title': '{} - Gent'.format(family),'family': family})
        else:
            return render(request, '404.html', {'user': request.user, 'title': '404 - Gent'})
    except e:
        print e
        return render(request, '500.html', {'user': request.user, 'title': '500 - Gent'})

@login_required()
def item(request, item_id):
    # Get item 
    try:
        item = Item.objects.get(id=item_id)

        if item:
            return render(request, 'item.html', {'user': request.user, 'title': '{} - Gent'.format(item),'item': item})
        else:
            return render(request, '404.html', {'user': request.user, 'title': '404 - Gent'})
    except:
        return render(request, '404.html', {'user': request.user, 'title': '404 - Gent'})

def ws_update_item_order(request):
    order = request.GET.get('order', '')
    id_list = order.split(',')

    try:
        for i, item_id in enumerate(id_list):
            item_id = id_list[i]
            item = Item.objects.get(id=item_id)
            item.order = i
            item.save()
        response = { 'status': 200 }
    except:
        response = { 'status': 500, 'message': "Couldn't update orders" }

    return JsonResponse(response)

def ws_toggle_item_complete(request):
    item_id = request.GET.get('item_id', '')

    try:
        item = Item.objects.get(id=item_id)
        if item.completed:
            item.completed = False
            item.date_completed = None
        else:
            item.completed = True
            item.date_completed = datetime.datetime.now()
        item.save()
        response = { 'status': 200 }
    except:
        response = { 'status': 500, 'message': "Couldn't toggle completion" }

    return JsonResponse(response)

def ws_item(request):
    item_id = request.GET.get('item_id', '')
    family = None

    # Special case for PUT
    req = None
    if request.method == 'POST':
        req = request.POST
    elif request.method == 'PUT':
        req = QueryDict(request.body)

    if req:
        title = req.get('title', '')
        family_id = req.get('family', '')
        family_name = req.get('family_box', '')
        datecreated = req.get('datecreated', '')
        datecompleted = req.get('datecompleted', '')
        notes = req.get('notes', '')

        # Load tags
        tag_list = req.get('tags', '')
        tags = []
        for tag in tag_list.split(', '):
            if tag != '':
                obj, created = Tag.objects.get_or_create(name=tag)
                tags.append(obj)

        # If new family
        if family_id == '' and family_name != '':
            try:
                husband, wife = family_name.split('/')
                args = {}
                if husband.strip() != '':
                    args['husband_name'] = husband.strip()

                if wife.strip() != '':
                    args['wife_name'] = wife.strip()

                family = Family(**args)
                family.save()
            except e:
                print e

    if item_id:
        item = Item.objects.get(id=item_id)

    if request.method == 'POST':
        # New item
        if title == '' or (family_id == '' and family is None):
            response = { 'status': 501, 'message': "Missing title or family" }
        else:
            try:
                if family is None:
                    family = Family.objects.get(id=family_id)
                item = Item(title=title, family=family, notes=notes)
                item.save()
                item.tags = tags
                item.save()

                response = { 'status': 200, 'id': item.id }
            except:
                response = { 'status': 500, 'message': "Couldn't create new item" }

    elif request.method == 'PUT':
        # Update item
        if title == '' or (family_id == '' and family is None):
            response = { 'status': 501, 'message': "Missing title or family" }
        else:
            try:
                if family is None:
                    family = Family.objects.get(id=family_id)

                item.title = title
                item.family = family
                item.notes = notes

                item.tags.clear()
                for tag in tags:
                    item.tags.add(tag)

                item.date_created = datecreated

                if datecompleted != '':
                    item.date_completed = datecompleted
                else:
                    item.date_completed = None

                item.save()

                response = { 'status': 200 }
            except e:
                response = { 'status': 500, 'message': "Couldn't update item" }

    elif request.method == 'DELETE':
        try:
            item.delete()
            response = { 'status': 200 }
        except e:
            response = { 'status': 500, 'message': "Couldn't delete item" }

    return JsonResponse(response)

def ws_family(request):
    family_id = request.GET.get('family_id', '')

    # Special case for PUT
    req = None
    if request.method == 'PUT':
        req = QueryDict(request.body)

    if req:
        husband_name = req.get('husband_name', '')
        husband_id = req.get('husband_id', '')
        wife_name = req.get('wife_name', '')
        wife_id = req.get('wife_id', '')
        datecreated = req.get('datecreated', '')
        datecompleted = req.get('datecompleted', '')
        notes = req.get('notes', '')

        # Load tags
        tag_list = req.get('tags', '')
        tags = []
        for tag in tag_list.split(', '):
            if tag != '':
                obj, created = Tag.objects.get_or_create(name=tag)
                tags.append(obj)

    if family_id:
        family = Family.objects.get(id=family_id)

    if request.method == 'PUT':
        # Update family
        if husband_name == '' and wife_name == '':
            response = { 'status': 501, 'message': "Missing husband or wife name" }
        else:
            try:
                family.husband_name = husband_name
                family.husband_id = husband_id
                family.wife_name = wife_name
                family.wife_id = wife_id
                family.notes = notes

                family.tags.clear()
                for tag in tags:
                    family.tags.add(tag)

                family.date_created = datecreated

                family.save()

                response = { 'status': 200 }
            except e:
                response = { 'status': 500, 'message': "Couldn't update family" }

    elif request.method == 'DELETE':
        try:
            family.delete()
            response = { 'status': 200 }
        except e:
            response = { 'status': 500, 'message': "Couldn't delete family" }

    return JsonResponse(response)

def ws_family_search(request):
    query = request.GET.get('query', '')
    suggestions = []

    # Search for family by husband/wife name/id
    families = Family.objects.filter(
                Q(husband_name__icontains=query)
                | Q(husband_id__icontains=query)
                | Q(wife_name__icontains=query)
                | Q(wife_id__icontains=query)
                ).distinct().order_by('husband_name', 'wife_name')

    for family in families:
        suggestions.append({
            'value': family.html(),
            'data': {
                'id': family.id,
                'subtitle': ' / '.join([family.husband_id, family.wife_id]),
            },
        })

    if query:
        response = {
            'query': query,
            'suggestions': suggestions,
        }
    else:
        response = { 'status': 500, 'message': "No query" }

    return JsonResponse(response)

def logout(request):
    return logout_then_login(request)
