"""accounts(유저관련) Module

이 모듈은 회원가입, 로그인, 회원생성(admin), 회원삭제(admin)
기능이 있다.  

"""

import logging
import json
import traceback

from django.template.response import TemplateResponse
from django.template.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponse,  HttpResponseNotFound,\
    HttpResponseRedirect
from django.db.utils import IntegrityError

from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from todolist.ErrClass import ErrClass
from accounts.models import User

from accounts.serializers import UserSerializer
import django_filters
from rest_framework.decorators import list_route
from util.utils import JSONResponse

logger = logging.getLogger('django_log')


class UserViewSet(viewsets.ModelViewSet):
    """
    Account Model 을 Restful API 로 관리 하는 ViewSet
    """
    
    ## admin 은 하면에 리스팅 하지 않는다. 
    queryset = User.objects.filter( is_superuser = 0 )
    serializer_class = UserSerializer
    
    ## admin 만 이 기능 사용가능
    permission_classes = (IsAdminUser  ,)
    
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields  = ( 'id', 'email')
    
    def create(self, request, *args, **kwargs):
        """
        HTTP POST Method 를 사용했을 때 호출되는 부분
        email 과 password 를 이용해서 user 를 생성한다. 
        """
        param_dict = request.data.copy()

        serializer = self.get_serializer(data=param_dict)
        if serializer.is_valid() == False:
            if 'username'  in serializer.errors:
                return ErrClass("DUPLICATED_EMAIL").response()
            return ErrClass('UNKNWON_ERROR').response()
        
        self.perform_create(serializer)
        user = serializer.instance
        user.is_active = True
        user.set_password(param_dict['password'])  ## 패스워드의 경우 Hashmode 을 이용하기 위해 해당 메소드를 이용한다. 
        user.save()
        result = ErrClass('NOERROR').toDict()
        return HttpResponse(json.dumps(result), content_type="application/json")
    
    @list_route(methods=['POST'])
    def deletelist(self, request):
        """
        HTTP POST Method 를 사용하고  deletelist 라는 path
        email 과 password 를 이용해서 user 를 생성한다.
        
        ids[] : 삭제하고 싶 
        """
        ids = request.POST.getlist("ids[]")
        objects = self.get_queryset().filter( id__in = ids )
        objects.delete()
        result = ErrClass('NOERROR').toDict()
        return HttpResponse(json.dumps(result), content_type="application/json")
    
    
    @list_route()
    def tablelist(self, request):
        """
        datatable.js 와 통신하는 함수
        """
        #TODO : 인젝션 방지를 위해 가능한 parameter 만 검사하는 코드 필요
        
        
         
        params = request.GET
         
        col_len = int(params.get('col_len', 0)) #전체 column 개수
        ord_col_len = int(params.get('ord_col_len', 0)) #정렬이 필요한 column 개수(현재는 1개만 가능) 
        start = int(params.get('start', 0)) # DB의 limit 에 해당하는 offset
        num = int(params.get('length', 25))  # 한 번에 가져와야 하는 리스트 개수
        
        column_list = []
        search_dict = {  }
        order_list = []
        
        # loop를 돌면서 column_list 정보와 필터링해야 하는 search_dict 정보를 가져온다. 
        for index in range(col_len):
            param_key = "columns[" +  str(index) + "][data]"
            col_name = params.get(param_key, None) 
            column_list.append( col_name )
            param_key = "columns[" +  str(index) + "][search][value]"
            search_value =  params.get(param_key, "")
            if  search_value:
                search_dict[col_name] = search_value
    
        # loop를 돌면서 정렬이 필요한 column 정보를 얻는다. 
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
        if len(search_dict): #filtering 해야 하는 정보가 있으면 filter
            obj_list = obj_list.filter( **search_dict  )
        
        
        obj_list = obj_list.order_by(*order_list) #데이터 정렬
        response_list = obj_list[start:(start+num)] # list 에 대한 limit start, start+num
        
        serializer = self.get_serializer(response_list, many=True)
  
        d = {
            "draw":params.get('draw',1),            
            "recordsTotal": obj_list.count(),
            "recordsFiltered": obj_list.count(), 
            "data" : serializer.data
        }
         
        return JSONResponse(self.request, d, status=200)


def _login(request):
    """ User login 기능 """
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
                result['email'] =  user.email
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

def _logout(request):
    logout(request)
    return HttpResponseRedirect("/")
        

def signup(request):
    """ 회원가입 기능 """
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
    