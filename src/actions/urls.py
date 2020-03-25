from django.contrib import admin
from django.urls import path, include


from rest_framework.routers import DefaultRouter
from .views import ItemViewSet, AuctionViewSet,BidViewSet

router = DefaultRouter()
router.register('item',ItemViewSet)
router.register('auction',AuctionViewSet)
router.register('bid',BidViewSet)


urlpatterns = [
    path('', include(router.urls)),
]