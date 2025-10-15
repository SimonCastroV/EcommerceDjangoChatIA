from django.urls import path
from . import views
from . import api_views
app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('api/', api_views.api_product_list, name='api_product_list'),
    path('api/<int:pk>/', api_views.api_product_detail, name='api_product_detail'),
]
