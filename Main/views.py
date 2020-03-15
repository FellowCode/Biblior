from django.http import Http404, JsonResponse
from django.shortcuts import render
import pprint

from utils.formatter import format_article, format_book, get_gost_article, get_gost_book
from utils.shortcuts import get_client_ip

pp = pprint.PrettyPrinter()

# filter types
# journal-article
# book-chapter
# book
# dissertation
from utils.search_query import get_search_query, search_crossref, citation_format, get_publication, get_publications


def index(request):
    return render(request, 'Main/Index.html')


def search(request):
    return render(request, 'Main/SearchPapers.html')


def papers_result(request):
    query = get_search_query(request, rows=40)
    search_crossref(query, get_client_ip(request))
    return render(request, 'Main/Papers.html', {'type': request.GET.get('search_type')})


def send_pubs(request):
    if request.is_ajax():
        result = get_publications(get_client_ip(request))
        if not result:
            return JsonResponse({'result': False})
        publications = []
        for item in result['message']['items']:
            if item['type'] == 'journal-article':
                publication = format_article(item)
            elif item['type'] == 'book':
                publication = format_book(item)
            else:
                publication = format_article(item)
            if len(publication['author']) > 0 and len(publication['title']) < 160:
                publications.append(publication)
        return JsonResponse({'result': True, 'publications': publications})
    raise Http404


def paper(request):
    doi = request.GET.get('DOI')
    #gost = citation_format(doi)[3:]
    publication = get_publication(doi)
    pp.pprint(publication)
    gost = ''
    if publication['type'] == 'journal-article':
        publication = format_article(publication)
        gost = get_gost_article(publication)
    elif publication['type'] == 'book':
        publication = format_book(publication)
        gost = get_gost_book(publication)
    elif publication['type'] == 'book-chapter':
        publication = format_article(publication)
        gost = get_gost_article(publication)
    return render(request, 'Main/Paper.html', {'type': publication['type'], 'gost': gost, 'publication': publication, 'doi': doi})


def create_citation(request):
    if request.is_ajax():
        pass
    raise Http404