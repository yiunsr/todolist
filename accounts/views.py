import logging
import json
import traceback

from django.template.response import TemplateResponse
from django.template.context_processors import csrf
from django.contrib.auth import authenticate, login
from django.http.response import HttpResponse,  HttpResponseNotFound
from django.db.utils import IntegrityError

from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from todolist.ErrClass import ErrClass
from accounts.models import User

from accounts.serializers import UserSerializer
import django_filters

logger = logging.getLogger('django_log')


class UserViewSet(viewsets.ModelViewSet):
    ## admin 제외 
    queryset = User.objects.filter( is_superuser = 0 )
    serializer_class = UserSerializer
    
    ## admin 만 이 기능 사용가능
    permission_classes = (IsAdminUser  ,)
    
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_fields  = ( 'id', 'email')


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
    