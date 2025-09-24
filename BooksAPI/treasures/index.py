from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register
from .models import Book
from django.conf import settings

@register(Book)
class ProductIndex(AlgoliaIndex):

    def get_queryset(self):
        return Book.objects.filter(public=True)

    


    fields = (
        'title', 
        'content',
        'author',
        'genre',
        'public',
        'price',
        'sale_price',
        'get_discount',
        'image_url',
    )


    settings = {
        'searchableAttributes': ['title', 'content', 'author','genre'],
        'attributesForFaceting': [
            'genre',
            'author'
            
        ],
    }


    tags = 'get_tags_list'
