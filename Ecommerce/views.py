from django.shortcuts import get_object_or_404
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView,ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.mixins import CreateModelMixin,ListModelMixin,DestroyModelMixin,UpdateModelMixin,RetrieveModelMixin
from rest_framework.viewsets import ModelViewSet
from .serializers import ProductSerializer,CollectionSerializer,ProductModelSerializer,CollectionModelSerializer,ReviewModelSerializer
from .models import Product,Collection,Review
from .filters import ProductFilter

#FUNCTION BASED VIEWS
@api_view(['GET','POST'])
def product_list(request):
    # StringRelatedField
    # products = Product.objects.select_related('collection').all()
    if request.method == 'GET':
        products = Product.objects.all()
        filter_set = ProductFilter(request.GET, queryset=products)
        search_param = request.GET.get('search', '')
        if search_param:
            filter_set = filter_set.filter(search_param)
        filtered_objects = filter_set.qs
        #Filter
        '''
        collection_id = request.query_params.get('collection_id')
        if collection_id is not None:
            products = Product.objects.filter(collection_id=collection_id)
        '''
        #serializer = ProductSerializer(products, many=True, context={'request':request})
        serializer = ProductModelSerializer(filtered_objects, many=True, context={'request':request})
        return Response( serializer.data, status = status.HTTP_200_OK )
    
    elif request.method == 'POST':
        serializer = ProductModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET','PUT','DELETE'])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'GET':
        serializer = ProductSerializer(product, many=False, context={'request': request})
        return Response( serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = ProductSerializer(instance=product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    elif request.method == 'DELETE':
        if product.orderitem_set.count() > 0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
@api_view(['GET','POST'])
def collection_list(request):
    if request.method == 'GET':
        collections = Collection.objects.annotate( products_count = Count('product'))
        serializer = CollectionSerializer(collections, many=True)
        return Response( serializer.data, status = status.HTTP_200_OK )
    elif request.method == 'POST':
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
@api_view(['GET'])
def collection_detail(request, pk):
    collection = get_object_or_404(Collection.objects.annotate( products_count = Count('product')), pk=pk)
    serializer = CollectionSerializer(collection , many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

#CLASS BASED VIEWS
#VIEWSET CLASS
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['title','description']
    ordering_fields = ['unit_price']
    
    #Filter
    '''
    def get_queryset(self):
        queryset = Product.objects.all()
        collection_id = self.request.query_params.get('collection_id')
        if collection_id is not None:
            queryset = Product.objects.filter(collection_id=collection_id)
        return queryset
    '''
    
    def perform_destroy(self, instance):
        if instance.orderitem_set.count() > 0:
            # You can raise an exception or handle the error in a way that suits your needs
            raise ValueError("Cannot delete product with associated order items.")
        instance.delete()
        
class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewModelSerializer
    #queryset = Review.objects.all()
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['Product_pk'])
        
    def get_serializer_context(self):
        product_id = self.kwargs.get('Product_pk')
        return {'product_id':product_id}
    
#APIVIEW CLASS 
''' ''' 
class ProductList(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductModelSerializer(products, many=True, context={'request':request})
        return Response( serializer.data, status = status.HTTP_200_OK )
    def post(self, request):
        serializer = ProductModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProductDetail(APIView):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, many=False, context={'request': request})
        return Response( serializer.data, status=status.HTTP_200_OK)
    def put(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(instance=product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitem_set.count() > 0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#MIXIN AND GENERICS
'''
class ProductList(ListModelMixin,CreateModelMixin,GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    
    def get(self, request):
        return self.list(request)
    def post(self, request):
        return self.create(request)
    
class ProductDetail(RetrieveModelMixin,DestroyModelMixin,UpdateModelMixin,GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    
    def get(self,request,pk):
        return self.retrieve(request,pk)
    def put(self,request,pk):
        return self.update(request,pk)
    def delete(self,request,pk):
        product = Product.objects.get(pk=pk)
        if product.orderitem_set.count() > 0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return self.destroy(request,pk)
'''
#GENERIC APIVIEWS
'''
class ProductList(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer

class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    
    def delete(self,request,pk):
        product = Product.objects.get(pk=pk)
        if product.orderitem_set.count() > 0:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return self.destroy(request,pk)
'''

    
