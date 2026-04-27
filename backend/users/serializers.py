from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # מושך את השדות הבסיסיים של המשתמש כדי שהריאקט יוכל להציג אותם
        fields = ['id', 'username', 'email', 'is_active', 'is_superuser', 'is_staff']