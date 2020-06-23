import urllib

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from Publications.models import Publication
from utils.search_query import *
import pprint
from urllib.parse import unquote
import json
import uuid


def search(request):
    return render(request, 'Publications/SearchForm.html')


def search_result(request):
    if request.GET.get('doi'):
        return redirect('/publication/?type=journal-article&doi='+urllib.parse.quote(request.GET.get('doi')))
    query = get_search_query(request, rows=60)
    uid = uuid.uuid4().hex
    search_crossref(query, uid)
    if request.GET.get('query_bibliographic'):
        search_query = 'Слова: ' + ', '.join(request.GET.get('query_bibliographic').split(' '))
    else:
        search_fields = []
        if request.GET.get('query_title'):
            search_fields.append('Название: '+request.GET.get('query_title'))
        if request.GET.get('query_authors'):
            search_fields.append('Авторы: ' + request.GET.get('query_authors'))
        if request.GET.get('query_container'):
            search_fields.append('Журнал/Сборник: ' + request.GET.get('query_container'))
        search_query = ', '.join(search_fields)
    return render(request, 'Publications/SearchResult.html', {'type': request.GET.get('search_type'), 'search_query': search_query, 'uid': uid})


def ajax_pubs(request):
    if request.is_ajax():
        result = get_publications(request.GET.get('uid'))
        if not result:
            return JsonResponse({'status': False})
        publications = []
        for item in result['message']['items']:
            publication = reformat(item)
            if len(publication['author']) > 0 and len(publication['title']) < 160:
                publications.append(publication)
        return JsonResponse({'status': True, 'publications': publications})
    raise Http404


def cite(request):
    doi = request.GET.get('doi')
    pub_type = request.GET.get('type')
    pub_id = request.GET.get('pub_id')
    source = request.GET.get('source', '')
    if request.method == 'POST':
        pub = dict(request.POST)
        for key, value in pub.items():
            pub[key] = value[0]
    else:
        pub = None
    data = {'type': pub_type, 'doi': doi, 'pub': pub, 'pub_id': pub_id, 'uid': uuid.uuid4().hex}
    if not pub and (pub_id or doi):
        if source == 'personal-area' and request.user.is_authenticated:
            if pub_id:
                pub = Publication.objects.get_or_none(user=request.user, id=pub_id)
            else:
                pub = Publication.objects.get_or_none(user=request.user, doi=doi)
            if pub:
                data['custom'] = True
                data['pub'] = pub
            else:
                get_publication(doi, data['uid'])
        else:
            get_publication(doi, data['uid'])
    return render(request, 'Publications/Citation.html', data)


def ajax_pub(request):
    if request.is_ajax():
        result = get_pub_result(request.GET.get('uid'))
        if not result:
            return JsonResponse({'status': False})
        if request.user.is_authenticated:
            Publication.set_pub(request.user, result['publication']).save()
        result['status'] = True
        pp.pprint(result)
        return JsonResponse(result)
    raise Http404


@login_required
def save_cite(request):
    if request.is_ajax():
        if request.method == 'POST':
            pub = dict(request.POST)
            for key, value in pub.items():
                pub[key] = value[0]
            Publication.set_pub(request.user, pub).save()
            return HttpResponse()
    raise Http404


def group_cite(request):
    print(list(map(int, json.loads(unquote(request.COOKIES.get('selected_cites'))))))
    sel_cites = list(map(int, json.loads(unquote(request.COOKIES.get('selected_cites')))))
    pubs = Publication.objects.filter(user=request.user, id__in=sel_cites).all()
    print(pubs)
    return render(request, 'Publications/GroupCitation.html', {'pubs': pubs})
