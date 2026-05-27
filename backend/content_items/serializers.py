from rest_framework import serializers
from .models import ContentItem

class ContentItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentItem
        fields = '__all__'

    def to_internal_value(self, data):
        # המרת הנתונים בכניסה כדי למנוע שגיאות בשמות שדות בין React ל-Django
        mutable_data = data.copy() if hasattr(data, 'copy') else dict(data)
        
        field_mappings = {
            'taskId': 'task', 'task_id': 'task', 'associated_task_id': 'task',
            'placeId': 'place', 'place_id': 'place',
            'regionId': 'region', 'region_id': 'region',
            'projectId': 'associated_project', 'project_id': 'associated_project', 'associated_project_id': 'associated_project' 
        }
        
        for frontend_field, backend_field in field_mappings.items():
            if frontend_field in mutable_data:
                mutable_data[backend_field] = mutable_data.pop(frontend_field)

        empty_fields_to_null = [
            'task', 'created_by', 'approved_by', 'place', 
            'region', 'associated_project', 'file_url', 'drive_link'
        ]
        
        for field in empty_fields_to_null:
            if mutable_data.get(field) == '':
                mutable_data[field] = None
                
        return super().to_internal_value(mutable_data)

    # 🔥 שורות הקסם החדשות: המרה בזמן יציאה מהבאקנד לפרונטאנד כדי להתאים לריאקט
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        
        # 1. הזרקת ה-IDs שהריאקט מחפש
        rep['region_id'] = instance.region_id
        rep['place_id'] = instance.place_id
        rep['associated_project_id'] = instance.associated_project_id
        
        # 2. תרגום הסטטוס לעברית בצורה אוטומטית (יחזיר "לסקירה", "טיוטה" וכו')
        rep['status'] = instance.get_approval_status_display()
        
        # 3. תרגום שדה התאריך כדי למנוע את קריסת הרינדור בריאקט
        rep['created_date'] = instance.created_at.isoformat() if instance.created_at else None
        
        return rep