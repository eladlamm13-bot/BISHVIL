from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    current_user, 
    UserViewSet, 
    OrgUserViewSet, 
    system_notifications, 
    task_views_dummy, 
    org_user_dummy, 
    check_calendar_dummy, 
    upsert_org_user_dummy
)

# הגדרת ה-Router עבור ה-ViewSets
router = DefaultRouter()
router.register(r'list', UserViewSet, basename='user-list')
router.register(r'org-list', OrgUserViewSet, basename='org-user-list')

urlpatterns = [
    # 1. הנתיב הקריטי שהריאקט מחפש כדי לזהות אותך (api/users/me/)
    path('me/', current_user, name='current-user'),
    
    # 2. כדורי ההרגעה (Dummy Endpoints) שהריאקט מחפש
    path('me/org-user/', org_user_dummy, name='org-user-dummy'),
    path('me/upsert-org-user/', upsert_org_user_dummy, name='upsert-org-user'),
    path('system-notifications/', system_notifications, name='system-notifications'),
    path('task-views/', task_views_dummy, name='task-views'),
    path('check-google-calendar/', check_calendar_dummy, name='check-calendar'),
    
    # 3. כל הנתיבים של ה-Router (כמו api/users/list/)
    path('', include(router.urls)),
]