#-*- coding: utf-8 -*-
import json
from django.http import HttpResponse
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler

_ERR_DICT = {
     "NOERROR" : [0 , u"정상"],
     "UNACTIVE_USER" : [10, u"로그인 할 수 없는 유저입니다. 관리자에게 확인 하세요."  ],
     "ID_OR_PASSWORD_WRONG" : [11, u"아이디 또는 패스워드가 올바르지 않습니다."  ],
     "DUPLICATED_EMAIL" : [12, u"해당 이메일로 이미 가입이 되어 있습니다."  ],
     "UNKNWON_ERROR" : [10000, u"알 수 없는 에러 입니다..",],
     "ERROR_WITH_DETAIL" : [10001, u"다음과 같은 에러가 발생했습니다.  %s " ,],
     
}

class ErrClass(APIException):
    status_code = 200
    #default_detail = 'Service temporarily unavailable, try again later.'
    
    errNo = None
    errMsg = None
    
    
    def __init__(self, errCode, errDetail = None,  status_code = 200 ):
        self.errNo = _ERR_DICT[errCode][0]
        self.errMsg = _ERR_DICT[errCode][1]
        if errDetail : 
            self.errMsg = self.errMsg % errDetail
            
        self.status_code = status_code
    
    def __str__(self):
        return json.dumps(   { "success" :  self.errNo == 0  ,  "code"  :   self.errNo, "message"  : self.errMsg   } )

        
    def msg(self):
        return self.errMsg
    
    def toDict(self):
        return   { "success" :  self.errNo == 0  ,  "code"  :   self.errNo, "message"  : self.errMsg   }
    
    def response(self):
        return HttpResponse( json.dumps(  { "success" :  self.errNo == 0  ,  "code"  :   self.errNo, "message"  : self.errMsg   }  ), content_type="application/json" , status = self.status_code )
            

