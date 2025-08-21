from rest_framework import serializers
from django.contrib.auth import get_user_model

Author = get_user_model()

class AuthorProductInlineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(
            view_name='books-details',
            lookup_field='pk',
            read_only=True
    )
    title = serializers.CharField(read_only=True)




class AuthorPublicSerializer(serializers.Serializer):
    authorname = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    other_books = serializers.SerializerMethodField(read_only=True)

    # class Meta:
    #     model = Author
    #     fields = [
    #         'authorname',
    #         'this_is_not_real',
    #         'id'
    #     ]

    def get_other_books(self, obj):
        author = obj
        my_books_qs = author.book_set.all()[:5]
        return AuthorProductInlineSerializer(my_books_qs, many=True, context=self.context).data