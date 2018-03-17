#-*- coding: utf-8 -*-
import decimal
import datetime
import json

import pytz

from django.http.response import HttpResponse
from todolist.settings import TIME_ZONE


def _json_dumps(obj):
    if isinstance(obj, decimal.Decimal):
        return  str(obj)
    if isinstance(obj, datetime.datetime):
        settingstime_zone = pytz.timezone(TIME_ZONE)
        newTime= obj.astimezone(settingstime_zone)
        return  newTime.strftime("%Y-%m-%d")
    raise TypeError


class JSONResponse(HttpResponse):
    """
    Return a JSON serialized HTTP response
    """
    def __init__(self, request, data, status=200):
        json_data = json.dumps(data, default=_json_dumps )
        super(JSONResponse, self).__init__(
            content=json_data,
            content_type='application/json',
            status=status,
        )
