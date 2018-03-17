import logging
from django.template.context_processors import csrf
import traceback
from django.template.response import TemplateResponse
from todolist.ErrClass import ErrClass

logger = logging.getLogger('django_log')

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
    