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
        'genre',
        'public',
        'price',
        'sale_price',
        'get_discount',
        'username',
        'image_url',
    )


    settings = {
        'searchableAttributes': ['title', 'content', 'username'],
        'attributesForFaceting': [
            'genre',
            'username'
        ],
    }


    tags = 'get_tags_list'

    def get_username(self, obj):
        try:
            return obj.posted_by.username if obj.posted_by else None
        except Exception as e:
            print(f"[Algolia] Failed to get authorname for Book {obj.pk}: {e}")
            return None
