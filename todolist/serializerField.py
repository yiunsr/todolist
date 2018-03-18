#-*- coding: utf-8 -*-
import datetime

from django.utils import timezone
from rest_framework import serializers
from rest_framework.utils import humanize_datetime

class DateTimeTzLocalField(serializers.DateTimeField):
    
    def to_representation(self, value):
        return self.to_native(value)
        
    def to_native(self, value):
        # 2017-12-31 10:00:00 형태
        if isinstance( value, datetime.datetime):
            if self.format == "unixtimestamp":
                return int(value.replace(tzinfo=timezone.utc).timestamp()) * 1000
            else:
                value = timezone.localtime(value)
                return value.strftime(self.format)
        
        # 2017-12-31 형태
        elif isinstance( value, datetime.date):
            return value.strftime(self.format)
        return value
    
    def to_internal_value(self, value):
        if value == "":
            return None
        
        if isinstance(value, datetime.date) and not isinstance(value, datetime.datetime):
            self.fail('date')

        if isinstance(value, datetime.datetime):
            return self.enforce_timezone(value)
        
        try:
            parsed = datetime.datetime.strptime( value , self.format )
            return self.enforce_timezone(parsed)
        except:
            humanized_format = humanize_datetime.datetime_formats(self.input_formats)
            self.fail('invalid', format=humanized_format)
            