from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('Playground/', include('Playground.urls'), name='Playground'),
    #path('Ecommerce/Api/', include('Ecommerce.urls'), name='Ecommerce'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
