from django.contrib import admin
from django.urls import path, include


from rest_framework.routers import DefaultRouter
from .views import ItemViewSet, AuctionViewSet

router = DefaultRouter()
router.register('item',ItemViewSet)
router.register('auction',AuctionViewSet)


urlpatterns = [
    path('', include(router.urls)),
]