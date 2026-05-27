from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContentItemViewSet # ודא שככה קוראים ל-ViewSet שלך בקובץ views.py

router = DefaultRouter()
# חשוב: ה-React מנסה לגשת לנתיב 'contents', אז אנחנו רושמים אותו בדיוק כך
# בקובץ content_items/urls.py

# שנה את השורה הזו:
router.register(r'contents', ContentItemViewSet, basename='content-item')

urlpatterns = [
    path('', include(router.urls)),
]