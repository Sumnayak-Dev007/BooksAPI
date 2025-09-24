from rest_framework import authentication,generics,mixins,permissions
from .models import Book
from rest_framework import status
from .serializers import BooksSerializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from api.authentication import TokenAuthentication
from api.permissions import IsStaffEditorPermission
from api.mixins import (
    AuthorQuerySetMixin,
    IsStaffEditorPermissionMixins,
    )
from api.mixins import IsStaffEditorPermissionMixins
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.

class BooksGetAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BooksSerializers


class BooksAPIView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BooksSerializers


class PostAPIView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BooksSerializers
    authentication_classes = [
    JWTAuthentication,
    authentication.SessionAuthentication,
    TokenAuthentication
    ]
    

    def perform_create(self, serializer):
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or title
        
        serializer.save(
            content=content,
            posted_by=self.request.user  
        )


class PutAPIView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BooksSerializers
    lookup_fiels = 'pk'

    def perform_update(self,serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title


class DeleteAPIView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BooksSerializers
    lookup_field = 'pk'

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Book deleted successfully."},
            status=status.HTTP_200_OK
        )

    def perform_destroy(self,instance):
        super().perform_destroy(instance)


      
        
# class ListCreateAPIView(
#     # AuthorQuerySetMixin,
#     # IsStaffEditorPermissionMixins,
#     generics.ListCreateAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BooksSerializers
#     authentication_classes = [
#     JWTAuthentication,
#     authentication.SessionAuthentication,
#     TokenAuthentication
#     ]

#     def perform_create(self,serializer):
#         title = serializer.validated_data.get('title')
#         content = serializer.validated_data.get('content') or None
#         if content is None:
#             content = title
#         serializer.save(author=self.request.user,content = content)



