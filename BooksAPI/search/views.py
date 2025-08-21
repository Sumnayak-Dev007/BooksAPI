from rest_framework import generics
from rest_framework.response import Response

from treasures.models import Book
from treasures.serializers import BooksSerializers

# Create your views here.


class SearchListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BooksSerializers

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        q = self.request.GET.get('q')
        results = Book.objects.none()
        if q is not None:
            results = qs.search(q)
        else:
            results = qs.filter(public=True)  # Also show only public if no query
        return results