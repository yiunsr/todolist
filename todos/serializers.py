from todolist.serializerField import DateTimeTzLocalField
from rest_framework import serializers
from accounts.models import User
from todos.models import Todo

class TodoSerializer(serializers.HyperlinkedModelSerializer):
    create_time  = DateTimeTzLocalField(format = "unixtimestamp" , read_only = True)
    
    class Meta:
        model = Todo
        fields = (  'id',  'priority' , 'text' , 'done' , 'create_time')
        read_only_fields = ('date_joined', 'last_login',  )
        