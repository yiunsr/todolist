from todolist.serializerField import DateTimeTzLocalField
from rest_framework import serializers
from accounts.models import User
from todos.models import Todo
from django.utils import timezone

class TodoSerializer(serializers.HyperlinkedModelSerializer):
    create_time  = DateTimeTzLocalField(format = "unixtimestamp" , read_only = True)
    day_of_week = serializers.SerializerMethodField()
    
    class Meta:
        model = Todo
        fields = (  'id',  'priority' , 'text' , 'done' , 'create_time', 'day_of_week')
    
    def get_day_of_week(self, obj):
        if obj.create_time:
            value = timezone.localtime(obj.create_time)
            return value.strftime("%w")
        else:
            return ""

class AdminTodoSerializer(serializers.HyperlinkedModelSerializer):
    create_time  = DateTimeTzLocalField(format = "unixtimestamp" , read_only = True)
    user_email = serializers.SerializerMethodField()
    
    class Meta:
        model = Todo
        fields = (  'id',  'priority' , 'text' , 'done' , 'create_time' , 'user_email')
        
    def get_user_email(self, obj):
        if obj.user:
            return   obj.user.email
        else:
            return ""