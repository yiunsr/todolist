
## todo 
* todo 관련 리스트업

### live demo
 * [http://todo.labstoo.com/](http://todo.labstoo.com/)


### 사용 라이브러리
* [vali-admin](https://github.com/pratikborsadiya/vali-admin)
  * Bootstrap4.0 템플릿

  
 ### 작업 설정
* requirements.txt 있는 파일에서 
  * pip install -r requirements.txt
* mysql, mariadb 설정
  * CONVERT_TZ 함수 지원을 위해 아래 작업 필요(아래 동작 안 했을 때 요일 기능 작동 안함) <br/>
  ```xml 
shell>mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root mysql
  ```
 