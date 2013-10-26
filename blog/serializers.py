from rest_framework import serializers

from .models import Category, Article, Tag


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        exclude = ('body',)
        read_only_fields = ('date',)
        #fields = ('id', 'title', 'author', 'date', 'category', 'tags')

    def validate(self, attrs):
        # do some validation with fields
        return attrs

    def validate_title(self, attrs, source):

        if len(attrs[source]) % 2 != 0:
            raise serializers.ValidationError("Title must contain even count of symbols.")
        return attrs


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name',)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name',)


###########################
## play with serializers ##
###########################

class Product(object):
    """
    Simple Python Class
    """

    def __init__(self, sku, price, title):
        self.sku = sku
        self.price = price
        self.title = title


class ProductSerializer(serializers.Serializer):
    """
    None Model-based serializer. For Python object
    """

    sku = serializers.IntegerField(max_value=5)
    price = serializers.FloatField()
    title = serializers.CharField(max_length=64)

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.sku = attrs.get('sku', instance.sku)
            instance.price = attrs.get('price', instance.price)
            instance.sku = attrs.get('sku', instance.sku)
            return instance
        return Product(**attrs)

    def validate_title(self, attrs, source):
        value = attrs[source]

        if "jaguar" in value.lower():
            raise serializers.ValidationError("Car name can not contain 'jaguar'")
        return attrs

    def validate(self, attrs):
        if attrs['sku'] > attrs['price']:
            raise serializers.ValidationError("Sku must be less than price.")
        return attrs















