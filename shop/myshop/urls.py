from django.urls import path
from . import views
from .views import form_handler

app_name = 'myshop'

urlpatterns = [
    path('product_list/', views.product_catalog, name='product_list'),
    path('search/', views.search, name='search'),
    path('searchprod/', views.search_product, name='search_product'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('conditions/', views.conditions, name='conditions'),
    path('', views.random_products, name='home'),
    path('form/', form_handler, name='form_handler'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('<slug:category_slug>/', views.product_catalog,
         name='product_list_by_category'
         ),
    path('<int:id>/<slug:slug>/', views.single_product, name='single-product'),
    path('review/<int:product_id>/<slug:slug>/', views.AddComments.as_view(), name='add_comments'),
    path('<int:id>/<slug:slug>/add_likes/', views.AddLike.as_view(), name='add_likes'),
]
