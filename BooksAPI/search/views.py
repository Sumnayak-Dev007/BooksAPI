from rest_framework import generics
from rest_framework.response import Response

from treasures.models import Book
from treasures.serializers import BooksSerializers
from algoliasearch.search.client import SearchClientSync 
# Create your views here.
client = SearchClientSync("GXRT6SL6EW", "f4c5d750cdb2326dc92310895f865e2d")

class SearchListView(generics.GenericAPIView):
    queryset = [] 

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')  
        tag = request.GET.get('tag')
        if not query and not tag:
            return Response({'error': 'At least one of "q" or "tag" must be provided.'}, status=400)

        try:
            filters = []
            if tag:
                filters.append(f'_tags:"{tag}"')

            filters_str = ' AND '.join(filters) if filters else None

            search_params = {
                "indexName": "gem_Book",
                "query": query,
                "hitsPerPage": 50,
            }

            if query:
                search_params["restrictSearchableAttributes"] = ["title"]

            if filters_str:
                search_params["filters"] = filters_str

            response = client.search({
                "requests": [search_params],
            })

            hits = response.to_dict()['results'][0]['hits']

            cleaned_hits = []
            for hit in hits:
                cleaned_hit = {
                    "objectID": hit.get("objectID"),
                    "title": hit.get("title"),
                    "content": hit.get("content"),
                    "public": hit.get("public"),
                    "price": hit.get("price"),
                    "sale_price": hit.get("sale_price"),
                    "discount": hit.get("get_discount"),
                    "user_username": hit.get("user_username"),
                    "_tags": hit.get("_tags", []),
                    "highlighted_title": hit.get("_highlightResult", {}).get("title", {}).get("value"),
                    "highlighted_user": hit.get("_highlightResult", {}).get("user_username", {}).get("value"),
                }
                cleaned_hits.append(cleaned_hit)

            return Response({"hits": cleaned_hits})

        except Exception as e:
            return Response({'error': str(e)}, status=500)

class SearchListDjangoView(generics.ListAPIView):
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