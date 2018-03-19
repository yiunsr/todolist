from todolist.serializerField import DateTimeTzLocalField
from rest_framework import serializers
from accounts.models import User
from todos.models import Todo

class UserSerializer(serializers.HyperlinkedModelSerializer):
    date_joined  = DateTimeTzLocalField(format = "%Y-%m-%d %H:%M:%S" , read_only = True)
    last_login  = DateTimeTzLocalField(format = "%Y-%m-%d %H:%M:%S" , read_only = True)
    total_todo = serializers.SerializerMethodField()
    avg_todo = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = (  'id',  'email' , 'date_joined' , 'last_login' , 'is_active', 'is_superuser' , 'total_todo' , 'avg_todo')
        read_only_fields = ('date_joined', 'last_login',  )
        
    def get_total_todo(self, obj):
        total = Todo.objects.filter( user = obj ).count()  #pylint: disable=no-member
        return total
        
    def get_avg_todo(self, obj):
        total = Todo.objects.filter( user = obj ).count()  #pylint: disable=no-member
        return   round(total / 7.0, 1)
        