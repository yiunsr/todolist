from todolist.serializerField import DateTimeTzLocalField
from rest_framework import serializers
from accounts.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    date_joined  = DateTimeTzLocalField(format = "%Y-%m-%d %H:%M:%S" , read_only = True)
    last_login  = DateTimeTzLocalField(format = "%Y-%m-%d %H:%M:%S" , read_only = True)
    
    class Meta:
        model = User
        fields = (  'id',  'email' , 'date_joined' , 'last_login' , 'is_active', 'is_superuser')
        read_only_fields = ('date_joined', 'last_login',  )
        