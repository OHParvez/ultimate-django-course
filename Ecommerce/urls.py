from django.urls import path,include
from .views import product_list,product_detail,collection_list,collection_detail
from .views import ProductList,ProductDetail
from .views import ProductViewSet,ReviewViewSet
from rest_framework.routers import SimpleRouter,DefaultRouter
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register(r'Products', ProductViewSet)
product_router = routers.NestedDefaultRouter(router, r'Products', lookup='Product')
product_router.register(r'Reviews', ReviewViewSet, basename='Product-Review')

urlpatterns = [
    #FUNCTION BASED
    path('products/', product_list, name='product_list'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
    path('collections/', collection_list, name='collection_list'),
    path('collection/<int:pk>/', collection_detail, name='collection_detail'),
    
    #CLASS BASED 
    path('Products/', ProductList.as_view() , name='ProductList'),
    path('Product/<int:pk>/', ProductDetail.as_view() , name='ProductDetail'),
    
    #ViewSets
    path(r'ViewSet/', include(router.urls)),
    path(r'ViewSet/', include(product_router.urls)), 
    
]


    

