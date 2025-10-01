# store/urls.py
from django.urls import path,include
from . import views

urlpatterns = [
   path('',views.store,name='store'),
   path('search/',views.search,name='search'),
   path('<slug:category_slug>/',views.store, name='product_by_category'),
   path('<slug:category_slug>/<slug:product_slug>/',views.product_detail, name='product_detail'),
   path('', include('store.urls')), 
   path('admin/', admin.site.urls),
  
] 
