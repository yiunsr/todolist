from __future__ import unicode_literals

from django.db import models
from accounts.models import User

class Todo(models.Model):  
    """ Todo  model 로 우선순위, 텍스트, 완료상태, 생성시간, 수정시간, 사용자 데이터가 존재한다. """
    
    HIGH = '3'
    MID = '2'
    LOW = '1'
    PRIORITY_CHOICES = ((HIGH, u'중요'),(MID, u'보통'),(LOW, u'낮음'))

    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default=MID, )
    text = models.TextField(null=False)
    done = models.BooleanField(default=False)
    
    create_time = models.DateTimeField()
    modify_time = models.DateTimeField(auto_now = True, null=True)
    
    user = models.ForeignKey(User, related_name="todo_user" , on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.text