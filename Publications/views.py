from django.http import JsonResponse, Http404, HttpResponse
from django.shortcuts import render

from Publications.models import Publication
from utils.formatter import reformat
from utils.search_query import get_search_query, search_crossref, get_publications, get_publication, get_pub_result
from utils.shortcuts import get_client_ip
import pprint
pp = pprint.PrettyPrinter()


def search(request):
    return render(request, 'Publications/SearchForm.html')


def search_result(request):
    query = get_search_query(request, rows=40)
    search_crossref(query, get_client_ip(request))
    return render(request, 'Publications/SearchResult.html', {'type': request.GET.get('search_type')})


def ajax_pubs(request):
    if request.is_ajax():
        result = get_publications(get_client_ip(request))
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
    get_publication(doi, get_client_ip(request))
    return render(request, 'Publications/Citation.html', {'type': pub_type, 'doi': doi})


def ajax_pub(request):
    if request.is_ajax():
        result = get_pub_result(get_client_ip(request))
        if not result:
            return JsonResponse({'status': False})
        Publication.set_pub(request.user, result['publication']).save()
        result['status'] = True
        pp.pprint(result)
        return JsonResponse(result)
    raise Http404


def save_cite(request):
    if request.is_ajax():
        if request.method == 'POST':
            pub = dict(request.POST)
            for key, value in pub.items():
                pub[key] = value[0]
            pp.pprint(pub)
            Publication.set_pub(request.user, pub).save()
            return HttpResponse()
    raise Http404
