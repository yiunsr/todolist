from django.test import TestCase
from pytest_django.fixtures import rf, client
from model_mommy import mommy

from accounts.models import User
from accounts.views import _login
from django.test.client import MULTIPART_CONTENT



class TestAccount(TestCase):
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
 
    def test_login_get(self):
        """ 로그인 화면 접근 가능성 테스트"""
        request = self.rf.get('/account/login')
        response = _login(request)
        assert response.status_code == 200
 
    def test_login_post(self):
        """ 로그인 테스트(ajax post)"""
        data = {"email" : "test01@test.com", "password" : "abcd1234"}
        response  = self.client.post('/account/login', data = data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        assert response.status_code == 200
        response_json =  response.json()
        assert response_json["success"] == True
        assert response_json["redirect_url"] == "/todo/list"
        
    def test_signup_post(self):
        """ 회원가입 테스트 """
        data = {"email" : "test_1000@test.com", "password" : "abcd1234"}
        response  = self.client.post('/account/signup', data = data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        assert response.status_code == 200
        response_json =  response.json()
        assert response_json["success"] == True
        
    
    def test_user_list_get(self):
        """ admin 으로 로그인 후, 회원정보 페이지 접근"""
        
        # admin 으로 로그인
        data = {"email" : "admin@test.com", "password" : "abcd1234"}
        response  = self.client.post('/account/login', data = data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        assert response.status_code == 200
        response_json =  response.json()
        assert response_json["success"] == True
        
        # 유저 리스트 페이지에 접근
        response  = self.client.get('/account/list')
        assert response.status_code == 200
        
    
    def test_user_list_tablelist(self):
        """ 회원정보 리스트 업 테스트 """        
        data = {"email" : "admin@test.com", "password" : "abcd1234"}
        response  = self.client.post('/account/login', data = data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        assert response.status_code == 200
        response_json =  response.json()
        assert response_json["success"] == True
        
        url = "/rest/account/tablelist/?draw=1&columns%5B0%5D%5Bdata%5D=id&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=false&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=id&columns%5B1%5D%5Bname%5D=&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=email&columns%5B2%5D%5Bname%5D=&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=date_joined&columns%5B3%5D%5Bname%5D=&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=last_login&columns%5B4%5D%5Bname%5D=&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=1&order%5B0%5D%5Bdir%5D=desc&start=0&length=10&search%5Bvalue%5D=&search%5Bregex%5D=false&col_len=5&ord_col_len=1&_=1521288893240"
        response  = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response_json =  response.json()
        
        ## 전체 데이터 리스트 3개( test01, test02, test03 세개의 유저)
        assert response_json["recordsTotal"] == 3
        assert response_json["recordsFiltered"] == 3
        
        assert response_json["data"][0]["email"] == "test03@test.com"
        assert response_json["data"][0]["date_joined"] == "2018-03-01 12:00:00"
        assert response_json["data"][0]["last_login"] == "2018-03-10 12:00:00"
        
        assert response_json["data"][1]["email"] == "test02@test.com"
        assert response_json["data"][1]["date_joined"] == "2018-03-01 11:00:00"
        assert response_json["data"][1]["last_login"] == "2018-03-10 11:00:00"
        
        assert response_json["data"][2]["email"] == "test01@test.com"
        assert response_json["data"][2]["date_joined"] == "2018-03-01 10:00:00"
        assert response_json["data"][2]["last_login"] == "2018-03-10 10:00:00"
        
        
    def test_user_create_delete(self):
        """ 회원정보 추가  삭제 테스트 테스트 """
        
        # admin 로그인        
        data = {"email" : "admin@test.com", "password" : "abcd1234"}
        response  = self.client.post('/account/login', data = data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        assert response.status_code == 200
        response_json =  response.json()
        assert response_json["success"] == True
        
        # user 추가 1
        data = { "email" : "test04@test.com", "password" : "abcd1234"  }
        response  = self.client.post('/rest/account/', data = data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        assert response.status_code == 200
        response_json =  response.json()
        assert response_json["success"] == True
        
        
        # user 추가 2
        data = { "email" : "test05@test.com", "password" : "abcd1234"  }
        response  = self.client.post('/rest/account/', data = data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        assert response.status_code == 200
        response_json =  response.json()
        assert response_json["success"] == True
        
        
        url = "/rest/account/tablelist/?draw=1&columns%5B0%5D%5Bdata%5D=id&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=false&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=id&columns%5B1%5D%5Bname%5D=&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=email&columns%5B2%5D%5Bname%5D=&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=date_joined&columns%5B3%5D%5Bname%5D=&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=last_login&columns%5B4%5D%5Bname%5D=&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=1&order%5B0%5D%5Bdir%5D=desc&start=0&length=10&search%5Bvalue%5D=&search%5Bregex%5D=false&col_len=5&ord_col_len=1&_=1521288893240"
        response  = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response_json =  response.json()
        
        ## 전체 데이터 리스트 5개( test01, test02, test03, test04, test05,  세개의 유저)
        assert response_json["recordsTotal"] == 5
        assert response_json["recordsFiltered"] == 5
        
        ## user 2개 삭제
        id1 = response_json["data"][0]["id"]
        data = { "ids[]" : (id1,) }
        
        response  = self.client.post("/rest/account/deletelist/", data = data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        assert response.status_code == 200
        response_json =  response.json()
        assert response_json["success"] == True
        
        
        url = "/rest/account/tablelist/?draw=1&columns%5B0%5D%5Bdata%5D=id&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=false&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=id&columns%5B1%5D%5Bname%5D=&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=email&columns%5B2%5D%5Bname%5D=&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=date_joined&columns%5B3%5D%5Bname%5D=&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=last_login&columns%5B4%5D%5Bname%5D=&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=1&order%5B0%5D%5Bdir%5D=desc&start=0&length=10&search%5Bvalue%5D=&search%5Bregex%5D=false&col_len=5&ord_col_len=1&_=1521288893240"
        response  = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response_json =  response.json()
        
        ## 전체 데이터 리스트 4개( test01, test02, test03, test04  세개의 유저)
        assert response_json["recordsTotal"] == 4
        assert response_json["recordsFiltered"] == 4
        
        
        
        