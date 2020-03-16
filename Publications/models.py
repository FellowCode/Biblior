from django.db import models

from Accounts.models import User
from utils.formatter import get_gost_book, get_gost_article
from utils.model_manager import MyManager


class Publication(models.Model):
    objects = MyManager()

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pubs')

    type = models.CharField(max_length=32)

    doi = models.CharField(max_length=32)
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
        return self.title[:min(len(self.title)-1, 60)] + '...'

    @staticmethod
    def set_pub(user, pub):
        self = Publication.objects.get_or_new(user=user, doi=pub['doi'])
        self.title = pub['title']
        self.author = pub['author']
        self.page = pub.get('page', '')

        self.issue = pub['issue']
        self.volume = pub['volume']
        self.issued = pub['issued']
        self.type = pub['type']
        self.container_title = pub.get('container_title', '')
        self.publisher = pub.get('publisher', '')
        return self

    def get_gost(self):
        pub = {
            'type': self.type,
            'title': self.title,
            'container_title': self.container_title,
            'author': self.author,
            'page': self.page,
            'publisher': self.publisher,
            'issue': str(self.issue),
            'issued': str(self.issued),
            'volume': str(self.volume),
        }
        if self.type == 'book':
            return get_gost_book(pub)
        return get_gost_article(pub)

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
        indexes = [models.Index(fields=['doi'])]
        ordering = ['-update_dt']
