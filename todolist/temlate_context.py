#-*- coding: utf-8 -*-

## CSS나 javascript 가 변경 될 경우, 자동으로 새로운  CSS 나 javascript 를 로딩 하도록 하기 위해 추가 됨
def global_context(request):
    cssver = "000001"
    jsver = "000001"
    return {
        "cssver" : cssver , 
        "jsver" : jsver ,
    } 
    