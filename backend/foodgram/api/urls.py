from django.urls import include, path
from rest_framework import routers

from users import views as user_views
from api import views

router = routers.DefaultRouter()
router.register(r'users', user_views.CustomUserViewSet, basename='users')
router.register(r'tags', views.TagViewSet, basename='tags')
router.register(
    r'ingredients', views.IngredientViewSet, basename='ingredients')
router.register(r'recipes', views.RecipeViewSet, basename='recipes')

urlpatterns = [
    path('recipes/<recipe_id>/favorite/',
         views.FavoriteViewSet.as_view({'post': 'favorite_create',
                                        'delete': 'favorite_delete'}),
         name='favorites'),
    path('recipes/<recipe_id>/shopping_cart/',
         views.ShoppingCartViewSet.as_view({'post': 'cart_create',
                                            'delete': 'cart_delete'}),
         name='shopping_carts'),
    path('recipes/download_shopping_cart/',
         views.ShoppingCartDownloadViewSet.as_view({'get': 'download'}),
         name='download_shopping_cart'),
    path('users/subscriptions/',
         user_views.SubscribeViewSet.as_view({'get': 'list'}),
         name='subscriptions'),
    path('users/<user_id>/subscribe/',
         user_views.SubscribeViewSet.as_view({'post': 'create',
                                              'delete': 'delete'}),
         name='subscribe'),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
