rus_alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

def reformat(publication):

    fpub = {'title': publication['title'][0], 'publisher': publication.get('publisher', ''),
             'issued': publication['issued']['date-parts'][0][0], 'volume': publication.get('volume', ''),
             'type': publication['type'], 'container_title': publication.get('container-title', [''])[0], 'page': publication.get('page', ''),
             'issue': publication.get('issue', ''), 'doi': publication['DOI'], 'url': publication['URL']}
    if len(publication.get('original-title', '')) > 0:
        fpub['title'] = publication['original-title'][0]

    fpub['author'] = format_authors(publication.get('author', []))

    return fpub


def format_authors(authors):
    fauthors = []
    rus_fauthors = []
    for i, author in enumerate(authors):
        if not author.get('family'):
            continue
        given = author.get('given', '').split(' ')
        initials = ''
        for word in given:
            if len(word)>0:
                initials += word[0] + '.'
        family = author.get('family', '')
        rus = any(c in rus_alphabet for c in family)
        if len(family) > 1:
            family = family[0].upper() + family[1:].lower()
        if rus:
            rus_fauthors.append('{} {}'.format(family, initials))
        else:
            fauthors.append('{} {}'.format(family, initials))
    if len(rus_fauthors) > 0:
        fauthors = rus_fauthors
    return ', '.join(a for a in fauthors if len(a) > 0 and a != ' ')


def get_gost_article(publication):
    gost = f"{publication['author']} {publication['title']} // {publication['container_title']}. – {publication['issued']}."
    if len(publication['volume']) > 0:
        gost += f" – Т. {publication['volume']}."
    if len(publication['issue']) > 0:
        gost += f" – №. {publication['issue']}."
    if len(publication['page']) > 0:
        gost += f" – С. {publication['page'].replace('-', '–')}."
    return gost


def get_gost_book(publication):
    gost = f"{publication['author']} {publication['title']}. – {publication['publisher']}, {publication['issued']}."
    return gost