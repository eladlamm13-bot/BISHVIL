from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlaceViewSet, PlaceTypeViewSet

# הגדרת הראוטר שיטפל בנתיבי ה-API באופן אוטומטי
router = DefaultRouter()
router.register(r'places', PlaceViewSet)
router.register(r'place-types', PlaceTypeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]