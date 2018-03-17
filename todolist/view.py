#-*- coding: utf-8 -*-
import logging
from django.http.response import HttpResponseRedirect
from django.template.response import TemplateResponse
import traceback
from todolist.ErrClass import ErrClass

logger = logging.getLogger('django_log')


def sample(request):
    try: 
        logger.info("/sample")
        if request.path.startswith("/rest") == False:
            c = {}
            response = TemplateResponse(request, 'sample.html', c)
            response.render()
            return response
    
    except Exception as e:
        logger.error(traceback.format_exc() )
        return ErrClass('UNKNWON_ERROR').response()

def main(request):
    logger.info("/main")
    
    ## 로그인 상태이면 todo 화면으로 바로 넘어간다.
    if request.user.is_authenticated:
        return HttpResponseRedirect('/todo/list') # 302
    
    ## 로그인 상태가 아니면 로그인 페이지로 
    return HttpResponseRedirect('/account/login') # 302