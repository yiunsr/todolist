import os 
from io import BytesIO


from django.test import TestCase
from pytest_django.fixtures import rf, client
from model_mommy import mommy

from accounts.models import User
from accounts.views import _login
from django.test.client import MULTIPART_CONTENT
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile


# Create your tests here.




class TestTodo(TestCase):
    def setUp(self):
        self.rf = rf()
        self.client = client()
        
        # abcd1234 가 hasing 데이터
        password = "pbkdf2_sha256$100000$7uSvfClog0In$V517cLrJU3ZgkWAcUyR13fWDpDL1uQFClKJEU3/kPmY="
        
        ## email : test01@test.com, password : abcd1234 인 유저 생성
        self.user1 = mommy.make(User, email="test01@test.com" , is_active= 1, password=password, date_joined = "2018-03-01 10:00:00", last_login= "2018-03-10 10:00:00")
        self.user2 = mommy.make(User, email="test02@test.com" , is_active= 1, password=password, date_joined = "2018-03-01 11:00:00", last_login= "2018-03-10 11:00:00")
        self.user3 = mommy.make(User, email="test03@test.com" , is_active= 1, password=password, date_joined = "2018-03-01 12:00:00", last_login= "2018-03-10 12:00:00")
        
        ## email : test01@test.com, password : abcd1234 인 admin 유저 생성
        self.admin = mommy.make(User, email="admin@test.com" , is_active= 1, password = password, is_superuser = 1, date_joined = "2018-03-01 10:00:00", last_login= "2018-03-01 10:00:00")
        
        
        
 
    def test_todolost_empty(self):
        """ 로그인 후 todo 화면에 접근"""
        
        ## test01 계정으로 로그인
        data = {"email" : "test01@test.com", "password" : "abcd1234"}
        response  = self.client.post('/account/login', data = data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        assert response.status_code == 200
        response_json =  response.json()
        assert response_json["success"] == True
        assert response_json["redirect_url"] == "/todo/list"
        
        response  = self.client.get('/rest/todo/', data = data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response_json =  response.json()
        assert response_json["count"] == 0
        
    def test_todolost_export(self):
        """ export 기능 테스트"""
        
        ## test01 계정으로 로그인
        data = {"email" : "test01@test.com", "password" : "abcd1234"}
        response  = self.client.post('/account/login', data = data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        assert response.status_code == 200
        response_json =  response.json()
        assert response_json["success"] == True
        assert response_json["redirect_url"] == "/todo/list"
        
        jsonData = """[{"id":"","priority":"2","text":"테스트 01","create_time":1521438718598,"done":false},{"id":"","priority":"2","text":"테스트 02","create_time":1521438722849,"done":true}]"""
        data = { "filetype" : "csv" , "jsonData" : jsonData }
        response  = self.client.get('/todo/export/', data = data)
        assert len(response.content) >  0
        assert response['Content-Type'] == "text/csv"
        
        data = { "filetype" : "excel" , "jsonData" : jsonData }
        response  = self.client.get('/todo/export/', data = data)
        assert len(response.content) >  0
        assert response['Content-Type'] == "application/vnd.ms-excel"
        
        data = { "filetype" : "json" , "jsonData" : jsonData }
        response  = self.client.get('/todo/export/', data = data)
        assert len(response.content) >  0
        assert response['Content-Type'] == "application/json"
        
 
    def test_todolost_import(self):
        """ import 기능 테스트"""
        ## test01 계정으로 로그인
        data = {"email" : "test01@test.com", "password" : "abcd1234"}
        response  = self.client.post('/account/login', data = data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        assert response.status_code == 200
        response_json =  response.json()
        assert response_json["success"] == True
        assert response_json["redirect_url"] == "/todo/list"
        
        
        ## CSV 파일 import 테스트
        todo_csv = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "res_test", "todolist_weektest.csv")
        
        file_data = File(open(todo_csv, 'rb'))
        upload_file = BytesIO(file_data.read())
        upload_file.name = "todolist_weektest.csv"
        
        response = self.client.post('/todo/import/', data = { "importfile": upload_file} )
        assert response.status_code == 200
        response_json =  response.json()
        assert len(response_json["jsonData"]) == 21
        assert response_json["jsonData"][0]["id"] == ""
        assert response_json["jsonData"][0]["priority"] == "1"
        assert response_json["jsonData"][0]["text"] == "일 01"
        assert response_json["jsonData"][0]["done"] == False
        
        assert response_json["jsonData"][1]["id"] == ""
        assert response_json["jsonData"][1]["priority"] == "2"
        assert response_json["jsonData"][1]["text"] == "일 02"
        assert response_json["jsonData"][1]["done"] == False
        
        
        ## Excel 파일 import 테스트
        todo_xls = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "res_test", "todolist_weektest.xls")
        
        file_data = File(open(todo_xls, 'rb'))
        upload_file = BytesIO(file_data.read())
        upload_file.name = "todolist_weektest.xls"
        
        response = self.client.post('/todo/import/', data = { "importfile": upload_file} )
        assert response.status_code == 200
        response_json =  response.json()
        assert len(response_json["jsonData"]) == 21
        assert response_json["jsonData"][0]["id"] == ""
        assert response_json["jsonData"][0]["priority"] == "1"
        assert response_json["jsonData"][0]["text"] == "일 01"
        assert response_json["jsonData"][0]["done"] == False
        
        assert response_json["jsonData"][1]["id"] == ""
        assert response_json["jsonData"][1]["priority"] == "2"
        assert response_json["jsonData"][1]["text"] == "일 02"
        assert response_json["jsonData"][1]["done"] == False
 
    def test_todolost_save(self):
        """ save 후, 데이터 가져오기"""
        
        ## test01 계정으로 로그인
        data = {"email" : "test01@test.com", "password" : "abcd1234"}
        response  = self.client.post('/account/login', data = data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        assert response.status_code == 200
        response_json =  response.json()
        assert response_json["success"] == True
        assert response_json["redirect_url"] == "/todo/list"
        
        jsonData = """ [{"id":"","priority":"2","text":"테스트 01","create_time":1521439736376,"done":false},{"id":"","priority":"2","text":"테스트 02","create_time":1521439739923,"done":true}] """
        data = { "jsonData" : jsonData }
        response  = self.client.post('/rest/todo/save/', data = data)
        response_json =  response.json()
        assert response_json["success"] == True
        
        response  = self.client.get('/rest/todo/', data = data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response_json =  response.json()
        assert response_json["count"] == 2
        assert response_json["results"][0]["id"] == 1
        assert response_json["results"][0]["priority"] == "2"
        assert response_json["results"][0]["text"] == u"테스트 01"
        assert response_json["results"][0]["done"] == False
        assert response_json["results"][0]["day_of_week"] == "1"
        
        assert response_json["results"][1]["id"] == 2
        assert response_json["results"][1]["priority"] == "2"
        assert response_json["results"][1]["text"] == u"테스트 02"
        assert response_json["results"][1]["done"] == True
        assert response_json["results"][1]["day_of_week"] == "1"
    
    
        #### Todo 리스트에서 id 1을 done으로 변경하고, priority 는 3으로 변경하고     id 2를 지운다. 
        jsonData = """ [{"id":1,"priority":"3","text":"테스트 01","create_time":1521439739923,"done":true}] """
        data = { "jsonData" : jsonData }
        response  = self.client.post('/rest/todo/save/', data = data)
        response_json =  response.json()
        assert response_json["success"] == True
        
        response  = self.client.get('/rest/todo/', data = data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response_json =  response.json()
        assert response_json["count"] == 1
        assert response_json["results"][0]["priority"] == "3"
        assert response_json["results"][0]["text"] == u"테스트 01"
        assert response_json["results"][0]["done"] == True
        assert response_json["results"][0]["day_of_week"] == "1"
        
        #### Todo 리스트를 다 지우고 저장한다. 
        jsonData = "[]"
        data = { "jsonData" : jsonData }
        response  = self.client.post('/rest/todo/save/', data = data)
        response_json =  response.json()
        assert response_json["success"] == True
        response  = self.client.get('/rest/todo/', data = data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response_json =  response.json()
        assert response_json["count"] == 0
    
    
    
    