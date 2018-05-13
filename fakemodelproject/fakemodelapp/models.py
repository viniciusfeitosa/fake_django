import collections
import requests
from django.db import models


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = collections.OrderedDict()

    def get(self, key):
        try:
            value = self.cache.pop(key)
            self.cache[key] = value
            return value
        except KeyError:
            return -1

    def set(self, key, value):
        try:
            self.cache.pop(key)
        except KeyError:
            if len(self.cache) >= self.capacity:
                self.cache.popitem(last=False)
        self.cache[key] = value


lru = LRUCache(500)


class EBSoaResourceManager(models.Manager):

    def all(self):
        posts = []
        response = requests.get('http://localhost:5000/api/storage')
        for obj in response.json()['objects']:
            post = Post(**obj)
            lru.set(str(post.id), post)
            posts.append(post)
        return posts

    def get(self, **kwargs):
        pk = str(kwargs['pk'])
        if lru.get(pk):
            print('from lru')
            return lru.get(pk)
        response = requests.get(
            'http://localhost:5000/api/storage/'+pk
        )
        return Post(**response.json())


class EBSoaResource(models.Model):

    def save(self, *args, **kwargs):
        value = {
            'title': self.title,
            'text': self.text,
        }
        if (self.id):
            response = requests.put(
                'http://localhost:5000/api/storage/'+str(self.id),
                json=value
            )
        else:
            response = requests.post(
                'http://localhost:5000/api/storage',
                json=value
            )
        self.__dict__.update(**response.json())
        lru.set(str(self.id), self)
        return self

    class Meta:
        abstract = True


class Post(EBSoaResource):
    objects = EBSoaResourceManager()
    title = models.CharField(max_length=200)
    text = models.TextField()

    def __str__(self):
        return self.title
