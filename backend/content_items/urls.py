from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContentItemViewSet # ודא שככה קוראים ל-ViewSet שלך בקובץ views.py

router = DefaultRouter()
# חשוב: ה-React מנסה לגשת לנתיב 'contents', אז אנחנו רושמים אותו בדיוק כך
router.register(r'contents', ContentItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]