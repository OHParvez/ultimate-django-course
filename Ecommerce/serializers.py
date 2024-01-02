from rest_framework import serializers
from decimal import *
from .models import Product,Collection,Review


#SERIALIZER
class CollectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    products_count = serializers.IntegerField()
    
class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    description = serializers.CharField()
    inventory = serializers.IntegerField()
    
    #Related Fields Serialization
    # 1. PrimaryKeyRelatedField
    '''
    collection = serializers.PrimaryKeyRelatedField(
       queryset = Collection.objects.all()
    )
    '''
    # 2. StringRelatedField
    '''
    collection = serializers.StringRelatedField()
    '''
    # 3. Nested Serialization
    ''' 
    collection = CollectionSerializer() 
    '''
    # 4. HyperlinkedRelatedField
    collection = serializers.HyperlinkedRelatedField(
        queryset = Collection.objects.all(),
        view_name = 'collection_detail'
    )
    #Addtional
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    
    def calculate_tax(self, product: Product):
        return (product.unit_price + product.unit_price * Decimal(.10))
    
    def validate(self, data):
        if data['price'] < 0:
            return serializers.ValidationError('Price mustbe greater than 0')

#MODELSERIALIZER
class CollectionModelSerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField()
    class Meta:
        model = Collection
        fields = ['id','title','products_count']

class ProductModelSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    
    def calculate_tax(self, product: Product):
        return (product.unit_price + product.unit_price * Decimal(.10))
    
    collection = serializers.HyperlinkedRelatedField(
        queryset = Collection.objects.all(),
        view_name = 'collection_detail'
    )
    class Meta:
        model = Product
        fields = ['id','title','price','description','slug','inventory','collection','price_with_tax']
    
    def validate(self, data):
        if data['price'] < 0:
            return serializers.ValidationError('Price mustbe greater than 0')

class ReviewModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id','date','name','description', 'product']


    


         