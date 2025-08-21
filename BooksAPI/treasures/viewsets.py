from rest_framework import viewsets, mixins
from .models import Book
from .serializers import BooksSerializers


class BooksViewset(viewsets.ModelViewSet):
    """
    get -> list -> Queryset  
    get -> retrieve -> Books Instance Detail View  
    post -> create -> New Instance  
    put -> Update  
    patch -> Partial Update  
    delete -> destroy  
    """
    queryset = Book.objects.all()
    serializer_class = BooksSerializers


class BooksGenericViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    """
    get -> list -> Queryset  
    get -> retrieve -> Book Instance Detail View  
    """
    queryset = Book.objects.all()
    serializer_class = BooksSerializers
    lookup_field = 'pk'  # default
