from django.db import models

from Accounts.models import User
from utils.formatter import get_gost_book, get_gost_article
from utils.model_manager import MyManager


class Publication(models.Model):
    objects = MyManager()
    # Поля таблицы публикации
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pubs')
    type = models.CharField(max_length=32)
    doi = models.CharField(max_length=64)
    url = models.URLField(default=None, null=True)
    title = models.CharField(max_length=256)
    container_title = models.CharField(max_length=128, blank=True)
    publisher = models.CharField(max_length=128, blank=True)
    author = models.CharField(max_length=128)
    issue = models.CharField(max_length=4, blank=True)
    volume = models.CharField(max_length=4, blank=True)
    issued = models.CharField(max_length=4)
    page = models.CharField(max_length=10, blank=True)
    update_dt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title[:min(len(self.title), 60)] + '...'

    @staticmethod
    def set_pub(user, pub):
        if pub.get('doi'):
            self = Publication.objects.get_or_new(user=user, doi=pub['doi'])
        elif pub.get('id'):
            self = Publication.objects.get_or_new(user=user, id=pub.get('id'))
        else:
            self = Publication(user=user)
        self.title = pub['title']
        self.author = pub['author']
        self.page = pub.get('page', '')
        self.url = pub['url']
        self.issue = pub['issue']
        self.volume = pub['volume']
        self.issued = pub['issued']
        self.type = pub['type']
        self.container_title = pub.get('container_title', '')
        self.publisher = pub.get('publisher', '')
        return self

    def to_dict(self):
        pub = {
            'doi': self.doi,
            'type': self.type,
            'title': self.title,
            'container_title': self.container_title,
            'author': self.author,
            'page': self.page,
            'publisher': self.publisher,
            'issue': self.issue,
            'issued': self.issued,
            'volume': self.volume,
        }
        return pub

    def get_gost(self):
        pub = self.to_dict()
        if self.type == 'book':
            return get_gost_book(pub)
        return get_gost_article(pub)

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
        indexes = [models.Index(fields=['doi'])]
        ordering = ['-update_dt']
