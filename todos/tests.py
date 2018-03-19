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
from todos.models import Todo


class TestTodo(TestCase):
    def setUp(self):
        self.rf = rf()
        self.client = client()
        
        # abcd1234 가 hasing 데이터
        password = "pbkdf2_sha256$100000$7uSvfClog0In$V517cLrJU3ZgkWAcUyR13fWDpDL1uQFClKJEU3/kPmY="
        
        ## email : test01@test.com, password : abcd1234 인 유저 생성
        self.user1 = mommy.make(User, id=1, email="test01@test.com" , is_active= 1, password=password, date_joined = "2018-03-01 10:00:00", last_login= "2018-03-10 10:00:00")
        self.user2 = mommy.make(User, id=2, email="test02@test.com" , is_active= 1, password=password, date_joined = "2018-03-01 11:00:00", last_login= "2018-03-10 11:00:00")
        self.user3 = mommy.make(User, id=3, email="test03@test.com" , is_active= 1, password=password, date_joined = "2018-03-01 12:00:00", last_login= "2018-03-10 12:00:00")
        
        ## email : test01@test.com, password : abcd1234 인 admin 유저 생성
        self.admin = mommy.make(User, email="admin@test.com" , is_active= 1, password = password, is_superuser = 1, date_joined = "2018-03-01 10:00:00", last_login= "2018-03-01 10:00:00")
        
        
        
 
    def test_0001_todolost_empty(self):
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
        
    def test_0002_todolost_export(self):
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
        
 
    def test_0003_todolost_import(self):
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
 
    def test_0004_todolost_save(self):
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
    
    def test_0005_dayofweeklist(self):
        """ 요일별 데이터 가져오기"""
        
        
        ## test01 계정으로 Todo 생성
        # 일요일
        todo01 = mommy.make(Todo, id = 1, priority= "1" , text = u"테스트  일 01",  done= False, create_time ="2018-03-11 04:31:30.749000",  modify_time= "2018-03-11 04:31:30.749000" ,  user = self.user1  )
        
        # 월요일 
        todo02 = mommy.make(Todo, id = 2, priority= "1" , text = u"테스트  월 01",  done= False, create_time ="2018-03-12 04:32:27.808000",  modify_time= "2018-03-12 04:32:27.808000" ,  user = self.user1  )
        todo03 = mommy.make(Todo, id = 3, priority= "1" , text = u"테스트  월 02",  done= True, create_time ="2018-03-12 05:32:27.808000",  modify_time= "2018-03-12 05:32:27.808000" ,  user = self.user1  )
        
        # 수요일 
        todo04 = mommy.make(Todo, id = 4, priority= "1" , text = u"테스트  수 01",  done= False, create_time ="2018-03-14 04:34:29.177000",  modify_time= "2018-03-14 04:34:29.177000" ,  user = self.user1  )
        
        ## test02 계정으로 Todo 생성
        # 금요일
        todo05 = mommy.make(Todo, id = 5, priority= "1" , text = u"테스트  금 01",  done= False, create_time ="2018-03-16 04:36:22.393000",  modify_time= "2018-03-16 04:36:22.393000" ,  user = self.user2  )
        
        ## test01 계정으로 로그인
        data = {"email" : "test01@test.com", "password" : "abcd1234"}
        response  = self.client.post('/account/login', data = data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        assert response.status_code == 200
        response_json =  response.json()
        assert response_json["success"] == True
        assert response_json["redirect_url"] == "/todo/list"
        
        response  = self.client.get('/rest/todo/', data = data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response_json =  response.json()
        assert response_json["count"] == 4
        
        assert response_json["results"][0]["id"] == 1
        assert response_json["results"][0]["day_of_week"] == "0" ## 일요일 체크
        
        assert response_json["results"][1]["id"] == 2
        assert response_json["results"][1]["day_of_week"] == "1" ## 월요일 체크
        
        assert response_json["results"][2]["id"] == 3
        assert response_json["results"][2]["day_of_week"] == "1" ## 월요일 체크
        
        assert response_json["results"][3]["id"] == 4
        assert response_json["results"][3]["day_of_week"] == "3" ## 수요일 체크
        
        
        ## admin 계정으로 로그인 후 admintodo 에서 잘 나오는지 테스트
        data = {"email" : "admin@test.com", "password" : "abcd1234"}
        response  = self.client.post('/account/login', data = data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        assert response.status_code == 200
        response_json =  response.json()
        assert response_json["success"] == True
        assert response_json["redirect_url"] == "/todo/list"
        
        response  = self.client.get('/rest/admintodo/', data = data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response_json =  response.json()
        assert response_json["count"] == 5
        
        assert response_json["results"][4]["id"] == 5
        assert response_json["results"][4]["day_of_week"] == "5" ## 금요일 체크
        
    
    