from rest_framework import serializers
from .models import Task, ProjectTask

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    def to_internal_value(self, data):
        # Create a mutable copy of the incoming data
        mutable_data = data.copy() if hasattr(data, 'copy') else dict(data)
        
        # המרת שמות שדות שהפרונטאנד שולח לשמות ש-Django מצפה להם
        field_mappings = {'regionId': 'region', 'region_id': 'region', 
                          'projectId': 'project', 'project_id': 'project',
                          'placeId': 'place', 'place_id': 'place'}
        for frontend_field, backend_field in field_mappings.items():
            if frontend_field in mutable_data:
                mutable_data[backend_field] = mutable_data.pop(frontend_field)

        # Convert empty strings sent by React into None (null) for dates and foreign keys
        for field in ['project', 'region', 'place', 'assigned_to', 'due_date']:
            if mutable_data.get(field) == '':
                mutable_data[field] = None
                
        return super().to_internal_value(mutable_data)

class ProjectTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTask
        fields = '__all__'

    def to_internal_value(self, data):
        mutable_data = data.copy() if hasattr(data, 'copy') else dict(data)
        
        # תיקון דומה גם למשימות של פרויקטים
        field_mappings = {'projectId': 'project', 'project_id': 'project'}
        for frontend_field, backend_field in field_mappings.items():
            if frontend_field in mutable_data:
                mutable_data[backend_field] = mutable_data.pop(frontend_field)

        for field in ['project', 'assigned_to', 'due_date']:
            if mutable_data.get(field) == '':
                mutable_data[field] = None
                
        return super().to_internal_value(mutable_data)