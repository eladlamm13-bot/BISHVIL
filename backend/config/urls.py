from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter
from users.views import OrgUserViewSet

# הוספת ראוטר ייעודי עבור נתיבים שיושבים ישירות תחת /api/
router = DefaultRouter()
router.register(r'org-users', OrgUserViewSet, basename='org-users')

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # משתמשים
    path('api/users/', include('users.urls')),

    # נתיב ישיר ל-org-users שהפרונטאנד מנסה לגשת אליו
    path('api/', include(router.urls)),

    # אזורים
    path('api/regions/', include('regions.urls')),

    # פרויקטים
    path('api/', include('projects.urls')),

    # מקומות ומשימות
    path('api/', include('places.urls')),
    path('api/', include('tasks.urls')),

    # תוכן
    path('api/', include('content_items.urls')),
    path('api/', include('dashboard.urls')),
]