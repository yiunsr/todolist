import logging
from django.template.context_processors import csrf
import traceback
from django.template.response import TemplateResponse
from todolist.ErrClass import ErrClass
from rest_framework import viewsets
from todos.models import Todo
from todos.serializers import TodoSerializer
from rest_framework.permissions import IsAuthenticated
import django_filters
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import list_route
import json
from django.http.response import HttpResponse


logger = logging.getLogger('django_log')


class TodoViewSet(viewsets.ModelViewSet):
    """
    Account Model 을 Restful API 로 관리 하는 ViewSet
    """
    
    queryset = Todo.objects.all()  #pylint: disable=no-member
    serializer_class = TodoSerializer
    
    ## admin 만 이 기능 사용가능
    permission_classes = (IsAuthenticated  ,)
    
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields  = ( 'id', 'priority')
    
    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)  #pylint: disable=no-member
    
    @list_route(methods=['POST'])
    def save(self, request):
        """
        HTTP POST Method 를 사용하고  save 라는 path 를 사용할 때
        데이터를 저장하는 함수
        저장하려는 데이터와 실제 DB에 저장된 데이터가 있을 때, 
        그 차이에 대해서만 저장하고 삭제한다. 
        """
        try:
            jsonDataString = request.POST.get("jsonData")
            jsonDataList = json.loads(jsonDataString)
            josnDataDict = {}  ## id 를 key  로,  나머지 데이터를 value 로하는 dict
            for item in jsonDataList:
                _id = item["id"]
                josnDataDict[_id] = item
            jsonDataSet = set(josnDataDict.keys())
            
            objects = self.get_queryset().filter(user=request.user)
            objectsDict = {} ## id 를 key로, 나머지 데이터를 value 로하는 dict
            for item in objects:
                _id = item.id
                objectsDict[_id] = item
            objectsSet = set(objectsDict.keys())
            
            ## jsonData 와 objects(DB) 를 비교해서
            ## jsonData 에만 존재, 데이터 추가
            itemToAdd = jsonDataSet - objectsSet
            for _id in itemToAdd:
                item = josnDataDict[_id]
                todo = Todo(user = request.user, priority = item["priority"], text = item["text"],  done = item["done"], create_time = item["create_time"])
                todo.save()
            
            ## objects에만 존재 데이터 삭제
            itemToDelete = objectsSet - jsonDataSet
            for _id in itemToDelete:
                item = objectsDict[_id]
                self.get_queryset().filter( id = _id ).delete()
                
            ## 양쪽에 다 존재하는 데이터의 done과 priority 상태 확인
            itemToUpdateCheck = objectsSet.union(jsonDataSet)
            for _id in itemToUpdateCheck:
                itemWeb = josnDataDict[_id]
                itemDB = objectsDict[_id]
                if itemWeb["done"] != itemDB.done or itemWeb["priority"] != itemDB.priority:
                    self.get_queryset().filter( id = _id ).update( done = itemWeb["done"], priority = itemWeb["priority"]  )
            
            result = ErrClass('NOERROR').toDict()
            return HttpResponse(json.dumps(result), content_type="application/json")
        except Exception as e:
            logger.error(traceback.format_exc() )
            return ErrClass('UNKNWON_ERROR').response()
        
   

@login_required
def _list(request):
    try: 
        logger.info("/todos/list")
        c = {}
        c.update(csrf(request))
        response = TemplateResponse(request, 'todos/list.html', c )
        response.render()
        return response
    
    except Exception as e:
        logger.error(traceback.format_exc() )
        return ErrClass('UNKNWON_ERROR').response()
    
    
@login_required
def export(request):
    try: 
        logger.info("/todos/list")
        c = {}
        c.update(csrf(request))
        response = TemplateResponse(request, 'todos/list.html', c )
        response.render()
        return response
    
    except Exception as e:
        logger.error(traceback.format_exc() )
        return ErrClass('UNKNWON_ERROR').response()