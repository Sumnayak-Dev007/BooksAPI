from django.db import models
from django.conf import settings
from django.db.models import Q
import random


User = settings.AUTH_USER_MODEL

TAGS_MODEL_VALUES = ['celestial', 'fantasy', 'facts', 'plays', 'metrics']


GENRE_CHOICES = [
    ('fiction', 'Fiction'),
    ('nonfiction', 'Non-Fiction'),
    ('fantasy', 'Fantasy'),
    ('mystery', 'Mystery'),
    ('romance', 'Romance'),
    ('sci-fi', 'Sci-Fi'),
    ('biography', 'Biography'),
    ('poetry', 'Poetry'),
    ('philosophical', 'Philosophical'),
    ('allegory', 'Allegory'),
]

class BookQuerySet(models.QuerySet):
    def is_public(self):
        return self.filter(public=True)

    def search(self, query):
        lookup = Q(title__icontains=query) | Q(content__icontains=query)
        return self.is_public().filter(lookup)

class BookManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return BookQuerySet(self.model, using=self._db)

    def search(self, query):
        return self.get_queryset().search(query)


class Book(models.Model):
    author = models.CharField(max_length=150)  
    posted_by = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField(null=False,blank=False)
    image = models.ImageField(upload_to='images/',blank=True, null=True)
    price = models.DecimalField(max_digits=5,decimal_places=2,default=100.25)
    public = models.BooleanField(default=True)
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES, default='fiction')

    objects = BookManager()


    def should_index(self):
        return self.public  

    def get_tags_list(self):
        return [random.choice(TAGS_MODEL_VALUES)]

    
    @property
    def sale_price(self):
        return "%.2f" %(float(self.price)*0.8)

    @property
    def username(self):
        return self.posted_by.username if self.posted_by else "Anonymous"


    def get_discount(self):
        return "12"

    @property
    def image_url(self):
        if self.image:
            return f"{settings.SITE_DOMAIN}{self.image.url}"
        return None




