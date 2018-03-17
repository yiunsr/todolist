import logging
import json
import traceback

from django.template.response import TemplateResponse
from django.template.context_processors import csrf
from django.contrib.auth import authenticate, login
from django.http.response import HttpResponse,  HttpResponseNotFound
from django.db.utils import IntegrityError

from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser

from todolist.ErrClass import ErrClass
from accounts.models import User

from accounts.serializers import UserSerializer
import django_filters
from rest_framework.decorators import list_route
from util.utils import JSONResponse
from pip._vendor.requests.models import Response

logger = logging.getLogger('django_log')


class UserViewSet(viewsets.ModelViewSet):
    ## admin 제외 
    queryset = User.objects.filter( is_superuser = 0 )
    serializer_class = UserSerializer
    
    ## admin 만 이 기능 사용가능
    permission_classes = (IsAdminUser  ,)
    
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields  = ( 'id', 'email')
    
    def create(self, request, *args, **kwargs):
        param_dict = request.data.copy()

        serializer = self.get_serializer(data=param_dict)
        if serializer.is_valid() == False:
            if 'username'  in serializer.errors:
                return ErrClass("DUPLICATED_EMAIL").response()
            return ErrClass('UNKNWON_ERROR').response()
        
        self.perform_create(serializer)
        user = serializer.instance
        user.is_active = True
        user.set_password(param_dict['password'])
        user.save()
        result = ErrClass('NOERROR').toDict()
        return HttpResponse(json.dumps(result), content_type="application/json")
    
    @list_route(methods=['DELETE'])
    def deletelist(self, request, *args, **kwargs ):
        ids = request.POST.getlist("ids[]")
        objects = self.get_queryset().filter( id__in = ids )
        objects.delete()
        result = ErrClass('NOERROR').toDict()
        return HttpResponse(json.dumps(result), content_type="application/json")
    
    
    @list_route()
    def tablelist(self, request, *args, **kwargs ):
        #TODO : 인젝션 방지를 위해 가능한 parameter 만 검사하는 코드 필요
         
        params = request.GET
         
        col_len = int(params.get('col_len', 0))
        ord_col_len = int(params.get('ord_col_len', 0))
        start = int(params.get('start', 0))
        num = int(params.get('length', 25))
        
        column_list = []
        search_dict = {  }
        order_list = []
        
        for index in range(col_len):
            param_key = "columns[" +  str(index) + "][data]"
            col_name = params.get(param_key, None) 
            column_list.append( col_name )
            param_key = "columns[" +  str(index) + "][search][value]"
            search_value =  params.get(param_key, "")
            if  search_value:
                search_dict[col_name] = search_value
    
        for index in range(ord_col_len):
            param_key = "order[" +  str(index) + "][column]"
            col_name = column_list[int(params.get(param_key, None))]
            order_dir_key = "order[" +  str(index) + "][dir]"
            order_dir = params.get(order_dir_key, None)
            if order_dir == "asc":
                order_list.append( col_name )
            else:
                order_list.append( "-" + col_name )
            
        
        obj_list = self.queryset
        if len(search_dict):
            obj_list = obj_list.filter( **search_dict  )
        
        
        obj_list = obj_list.order_by(*order_list)
        response_list = obj_list[start:(start+num)]
        
        serializer = self.get_serializer(response_list, many=True)
  
        d = {
            "draw":params.get('draw',1),            
            "recordsTotal": obj_list.count(),
            "recordsFiltered": obj_list.count(), 
            "data" : serializer.data
        }
         
        return JSONResponse(self.request, d, status=200)


def _login(request):
    try: 
        logger.info("/account/login")
        if  request.is_ajax() == False:
            c = {}
            c.update(csrf(request))
            response = TemplateResponse(request, 'accounts/login.html', c )
            response.render()
            return response
        
        email = request.POST.get('email')
        password = request.POST.get('password')
        next = request.POST.get('next')
        user = authenticate(username=email, password=password)
        if user is not None:  ## 로그인 체크
            if user.is_active:  ## 유저 상태 active 인지 검사(admin 이 false 설정을 해서 로그인을 막아 놓았을 수 있다.)
                login(request, user)
                result = ErrClass('NOERROR').toDict()
                result['user_index'] = user.pk
                result['email'] =  user.username
                if next:
                    result['redirect_url'] = next
                else:
                    result['redirect_url'] = "/todo/list"
                return HttpResponse(json.dumps(result), content_type="application/json")
            return ErrClass("UNACTIVE_USER").response()
       
        else:
            return ErrClass("ID_OR_PASSWORD_WRONG").response()
    
    except Exception as e:
        logger.error(traceback.format_exc() )
        return ErrClass('UNKNWON_ERROR').response()



def signup(request):
    try: 
        logger.info("/account/signup")
        if  request.is_ajax() == False:
            return HttpResponseNotFound('<h1>Page not found</h1>')
        
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.create_user(email, password)
        
        if user is not None: #Verify form's content existence
            if user.is_active: #Verify validity
                login(request, user)
                result = ErrClass('NOERROR').toDict()
                result['user_index'] = user.pk
                result['email'] =  user.email
                return HttpResponse(json.dumps(result), content_type="application/json")
       
        else:
            return ErrClass("ID_OR_PASSWORD_MISMATCH").response()
    
    except IntegrityError as e:
        logger.error(traceback.format_exc() )
        ## 동일 이메일 중복으로 인한 에러
        if "1062" in str(e):
            return ErrClass('DUPLICATED_EMAIL').response()
        
        return ErrClass('UNKNWON_ERROR').response()
    
    except Exception as e:
        logger.error(traceback.format_exc() )
        return ErrClass('UNKNWON_ERROR').response()
    
def _list(request):
    try: 
        logger.info("/account/list")
        c = {}
        c.update(csrf(request))
        response = TemplateResponse(request, 'accounts/list.html', c )
        response.render()
        return response
    
    except Exception as e:
        logger.error(traceback.format_exc() )
        return ErrClass('UNKNWON_ERROR').response()
    