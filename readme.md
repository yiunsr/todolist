
## todo 
* todo 관련 리스트업

### live demo
* [http://todo.labstoo.com/](http://todo.labstoo.com/)

### 실행
* python3 버전
* requirements.txt 있는 파일에 있는 라이브러리 설치
  * pip install -r requirements.txt
* 테스트 서버 동작
  * venv  환경일경우 해당 파이썬 환경을 active 한 후 
  * python manage.py runserver
*  http://127.0.0.1:8000 으로 접속
* DB는 외부 mariadb 를 사용함


### 서버 stack
 * python 3.5.2
 * django 2.0.3
 * djangorestframework
 * openpyxl 2.5.1 : 파이썬 엑셀 write, read 라이브러리
 * pytest, pytest-django, model-mommy : Unittest 환경
 * Nginx 1.10.3
 * Uwsgi  2.0.17
 * MariaDB 10.0.34
 * Ubunt 16.04


### 사용 라이브러리
* [vali-admin](https://github.com/pratikborsadiya/vali-admin)
  * Bootstrap4.0 템플릿
* [lodash](https://lodash.com/)
  * 자바스크립트 유틸리티 라이브러리(List, Dict 형 데이터를 추출, 정렬 하는 라이브러리)
* [datatable.js](https://datatables.net/)
  * 테이블로 이루어진 대부분은 이 라이브러리를 이용함
  * 리스트형 데이터의 기본적인 pagination, sort 기능제공


  
### 개발환경 설정
* requirements.txt 있는 파일에서 
  * pip install -r requirements.txt
* mysql, mariadb 설정
  * CONVERT_TZ 함수 지원을 위해 아래 작업 필요(아래 동작 안 했을 때 요일 기능 작동 안함) <br/>
  ```xml 
shell>mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root mysql
  ```
* DB 설정
  * /todolist/todolist/__init__.py  에 DB 경로 설정 필요   
  * DB 스키마와 기본 데이터는 아래 링크 데이터를 import 해서 이용한다. 
    * [DB Dump](https://github.com/yiunsr/todolist/blob/master/res/todo_Dump20180319.sql)
  
  
 
 
 