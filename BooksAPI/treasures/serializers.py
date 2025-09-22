from rest_framework import serializers
from rest_framework.reverse import reverse
from api.serializers import AuthorPublicSerializer
from .models import Book

class BooksSerializers(serializers.ModelSerializer):
    
    # my_author_data = serializers.SerializerMethodField(read_only=True)
    posted_by = serializers.CharField(source="posted_by.username", read_only=True)
    image_url = serializers.SerializerMethodField()
    my_discount = serializers.SerializerMethodField(read_only=True)
    edit_url = serializers.SerializerMethodField(read_only=True)
    url = serializers.HyperlinkedIdentityField(
            view_name='books-details',
            lookup_field='pk')
    # name = serializers.CharField(source='title',read_only=True)

    
    class Meta:
        model = Book
        fields = [
            'pk',
            'title',
            'author',
            'content',
            'genre',
            'price',
            'sale_price',
            'my_discount',
            'public',
            'edit_url',
            'url',
            'image_url',
            'posted_by',
           
        ]

    
    def validate_title(self,value):
        qs = Book.objects.filter(title__iexact=value)
        if qs.exists():
            raise serializers.ValidationError(f'{value} is already a Books title')
        return value
    
    def create(self, validated_data):
        email = validated_data.pop('email', None)
        obj = super().create(validated_data)
        if email:
            print(f"Email captured: {email}")
        return obj


    def update(self,instance,validated_data):
        email = validated_data.pop('email')
        return super().update(instance,validated_data)


    def get_edit_url(self,obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("books-edit",kwargs={"pk":obj.pk},request=request)


    def get_my_discount(self,obj):
        return obj.get_discount()


    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image:
            url = obj.image.url
            if request is not None:
                return request.build_absolute_uri(url)
            return url
        return None

    