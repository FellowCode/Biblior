import requests
import json
from .decorators import make_async
from .formatter import get_gost_article, reformat, get_gost_book

search_results = {}
pub_results = {}

def get_search_query(request, rows=20):
    search_type = request.GET.get('search_type')
    if search_type:
        elements = 'select=DOI,author,container-title,original-title,title,issued,publisher,subject,type,page,volume,issue'
        sort='sort=score&order=desc'
        query = f'{elements}&{sort}&rows={rows}&filter=type:{search_type}'
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
        return query
    return None


@make_async
def search_crossref(query, user_ip):
    url = f'https://api.crossref.org/works?{query}'
    r = requests.get(url)
    search_results[user_ip] = json.loads(r.content.decode('utf-8'))


def get_publications(user_ip):
    return search_results.pop(user_ip, None)


def citation_format(doi):
    url = f'https://citation.crosscite.org/format?doi={doi}&style=gost-r-7-0-5-2008&lang=ru-RU'
    r = requests.get(url)
    return r.content.decode('utf-8')


@make_async
def get_publication(doi, user_ip):
    url = f'http://api.crossref.org/works/{doi}'
    r = requests.get(url)
    publication = json.loads(r.content.decode('utf-8'))['message']
    publication = reformat(publication)
    if publication['type'] == 'book':
        gost = get_gost_book(publication)
    else:
        gost = get_gost_article(publication)
    pub_results[user_ip] = {'gost': gost, 'publication': publication}


def get_pub_result(user_ip):
    return pub_results.pop(user_ip, None)
