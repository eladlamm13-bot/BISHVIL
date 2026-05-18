from rest_framework import serializers
from .models import ContentItem

class ContentItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentItem
        fields = '__all__'

    def to_internal_value(self, data):
        # המרת הנתונים כדי למנוע שגיאות בשמות שדות בין React ל-Django
        mutable_data = data.copy() if hasattr(data, 'copy') else dict(data)
        
        # המרת שמות שדות שהפרונטאנד עלול לשלוח
        field_mappings = {
            'taskId': 'task', 'task_id': 'task',
            'placeId': 'place', 'place_id': 'place',
            'regionId': 'region', 'region_id': 'region',
            'projectId': 'project', 'project_id': 'project'
        }
        
        for frontend_field, backend_field in field_mappings.items():
            if frontend_field in mutable_data:
                mutable_data[backend_field] = mutable_data.pop(frontend_field)

        # ✅ לרשימה נוספו file_url ו-drive_link כדי להמיר טקסט ריק ("") ל-None חוקי בדג'נגו
        empty_fields_to_null = [
            'task', 'created_by', 'approved_by', 'place', 
            'region', 'project', 'file_url', 'drive_link'
        ]
        
        for field in empty_fields_to_null:
            if mutable_data.get(field) == '':
                mutable_data[field] = None
                
        return super().to_internal_value(mutable_data)