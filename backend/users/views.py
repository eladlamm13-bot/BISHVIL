from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()

# ---------------------------------------------------------
# 1. הפונקציה המקורית שלנו לזיהוי המשתמש המחובר (הריאקט חייב אותה!)
# ---------------------------------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = request.user
    role = 'admin' if user.is_superuser else 'worker'
    
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        # הוספנו את השדות שהריאקט מחפש כדי לשחרר את החסימה
        'first_name': user.first_name or 'מעוז',
        'last_name': user.last_name or 'דמרי',
        'phone': '0547695452',
        'is_active': user.is_active,
        'is_superuser': user.is_superuser,
        'is_staff': user.is_staff,
        'role': role,
    })

# ---------------------------------------------------------
# 2. המחלקות החדשות שהשרת מחפש כדי לשלוף רשימות משתמשים
# ---------------------------------------------------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class OrgUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

# ---------------------------------------------------------
# 3. כדורי הרגעה לריאקט (Dummy Endpoints)
# ---------------------------------------------------------

# פונקציה זמנית כדי שהריאקט לא ייתקע בחיפוש התראות
@api_view(['GET'])
def system_notifications(request):
    return Response([])  # מחזיר רשימה ריקה - "אין התראות כרגע"

# כדור הרגעה לתצוגות משימה
@api_view(['GET'])
def task_views_dummy(request):
    return Response([])  # מחזיר מערך ריק של תצוגות

# כדור הרגעה להגדרות משתמש ארגוני (מעודכן עם פרטים מזהים)
@api_view(['GET', 'PATCH'])
def org_user_dummy(request):
    return Response({
        "id": 1,
        "first_name": "מעוז",
        "last_name": "דמרי",
        "phone": "0547695452",
        "is_profile_complete": True 
    }) 

# כדור הרגעה לחיבור יומן גוגל
@api_view(['POST'])
def check_calendar_dummy(request):
    return Response({"connected": False})  # אומר לריאקט "היומן כרגע לא מחובר"

# כדור הרגעה לשמירת משתמש ארגוני (כדי שהריאקט ייתן להיכנס למערכת)
@api_view(['POST'])
def upsert_org_user_dummy(request):
    # אנחנו פשוט מחזירים תשובה חיובית שהכל עבר בשלום
    return Response({"success": True, "message": "User updated successfully"})