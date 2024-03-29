from django.urls import path
import search.views as s_views

app_name = 'search'

urlpatterns = [
    path('produits/rechercher', s_views.search_product_view, name='searchProductPage'),
    path('produits/recherche_avancee', s_views.advanced_search_view, name='advancedSearchPage')
]
