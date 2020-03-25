import requests
import json
from .decorators import make_async
from .formatter import get_gost_article, reformat, get_gost_book
import pprint
import xmltodict

pp = pprint.PrettyPrinter()

search_results = {}
pub_results = {}

def get_search_query(request, rows=20):
    search_type = request.GET.get('search_type')
    if search_type:
        elements = 'select=DOI,URL,author,container-title,original-title,title,issued,publisher,subject,type,page,volume,issue'
        sort = 'sort=score&order=desc'
        query = f'{elements}&{sort}&rows={rows}&filter=type:{search_type},has-full-text:true'
        query_bibliographic = request.GET.get('query_bibliographic')
        if query_bibliographic:
            return query + f'&query.bibliographic={query_bibliographic}'
        year_from = request.GET.get('year_from')
        if year_from:
            query += f',from-created-date:{year_from}'
        year_until = request.GET.get('year_until')
        if year_until:
            query += f',until-created-date:{year_until}'
        title = request.GET.get('query_title')
        if title:
            query += f'&query={title}'
        authors = request.GET.get('query_authors')
        if authors:
            query += f'&query.authors={authors}'
        query_container = request.GET.get('query_container')
        if query_container:
            query += f'&query.container-title={query_container}'
        return query
    return None


def get_search_query_arxiv(request, max_results=40):
    query_bibliographic = request.GET.get('query_bibliographic')
    if query_bibliographic:
        return f'search_query=all:\"{query_bibliographic}\"&max_results={max_results}'


@make_async
def search_arxiv(query, uid):
    url = f'http://export.arxiv.org/api/query?{query}'
    r = requests.get(url)
    print(url)
    pp.pprint(json.dumps(xmltodict.parse(r.content.decode('utf-8'))))


@make_async
def search_crossref(query, uid):
    url = f'https://api.crossref.org/works?{query}'
    r = requests.get(url)
    search_results[uid] = json.loads(r.content.decode('utf-8'))
    pp.pprint(search_results[uid])


def get_publications(uid):
    return search_results.pop(uid, None)


def citation_format(doi):
    url = f'https://citation.crosscite.org/format?doi={doi}&style=gost-r-7-0-5-2008&lang=ru-RU'
    r = requests.get(url)
    return r.content.decode('utf-8')


@make_async
def get_publication(doi, uid):
    url = f'http://api.crossref.org/works/{doi}'
    r = requests.get(url)
    publication = json.loads(r.content.decode('utf-8'))['message']
    publication = reformat(publication)
    if publication['type'] == 'book':
        gost = get_gost_book(publication)
    else:
        gost = get_gost_article(publication)
    pub_results[uid] = {'gost': gost, 'publication': publication}


def get_pub_result(uid):
    return pub_results.pop(uid, None)
