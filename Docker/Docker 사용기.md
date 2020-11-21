# Docker 사용기

> 이론적인 부분보다 직접 사용하면서 느낀점에 대한 회고 입니다.



## Docker 기초

> 명령어, 



### 명령어

1. `docker ps`: 실행중인 컨테이너 목록 출력
2. `docker images`: 존재하는 imge 목록 출력
3. `docker build <옵션> .`: 현재 dir에 있는 Dockerfile을 build한다.
   1. `-t 이름:태그`: image의 이름, 태그를 설정하여 build한다.
4. `docker image prune`: 이름이 None인 image들을 삭제한다.
   1. 연습하는 과정에서 None image가 많이 생겨서...





### Django Dockerfile

```dockerfile
FROM python:3.8.6
ENV PYTHONUNBUFFERED=1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --upgrade pip 
RUN pip install mysqlclient 
RUN pip install -r requirements.txt
COPY . /code/
RUN apt-get update
RUN apt-get install cron -y
RUN apt-get install 'ffmpeg' 'libsm6' 'libxext6'  -y
```



1. Backend 개발자간 python을 맞춤.

2. Setting `PYTHONUNBUFFERED` to a non empty value ensures that the **python output is sent straight to terminal** (e.g. your container log) without being first buffered and that you can see the output of your application (e.g. django logs) in real time

   요약: python log가 buffer없이 terminal로 출력된다!
   [PYTHONUNBUFFERED 설명](https://stackoverflow.com/questions/59812009/what-is-the-use-of-pythonunbuffered-in-docker-file)

3. `/`경로에 `code`폴더를 만든다.

4. 작업 폴더를 설정

5. Django의 requirements.txt를 `/code`에 복사한다.

6. pip upgrade

7. DB로 mysql을 사용하였다. mysql을 위한 orm을 설치한다.
   관련 error:[native dependencies](https://stackoverflow.com/questions/53854987/django-over-docker-does-not-install-mysqlclient/53855801)
   방법 2가지

   1. mysqlclient has native dependencies that must be installed before you can `pip install` it. 

      `pip install requirements.txt` 전에 `pip install`한다.

   2. `mysqlclient`대신 `mysql-connector-python`을 사용한다. `mysql-connector-python`은 pure python library이며, native dependencies를 포함하고 있지 않다.

8. Django에 필요한 requirements.txt 설치

9. `Django app`및 파일 복사

10. cron, opencv를 사용하기 위한 update

11. cron 설치, 설치 중간 yes를 위해 `-y`를 넣는다.

12. opencv를 경로 에러를 고치기 위해



### Docker-compose.yml

```dockerfile
version: '3.8'
services:

  backend1:
    image: void_back:0.1
    command: bash -c "pip install -r requirements.txt
      && python manage.py makemigrations
      && python manage.py migrate
      && gunicorn --bind 0:8001 bexperts.wsgi:application"
    volumes:
      - ./Django:/code
    expose:
      - "8001"
    depends_on:
      - db
    restart: always
  
  db:
    image: mysql
    
    container_name: mysql_service
    environment: 
      MYSQL_ROOT_PASSWORD: "${DB_ROOT_PASSWORD}"
      MYSQL_DATABASE: "${DB_DATABASE}"
      MYSQL_USER: "${DB_USER}"
      MYSQL_PASSWORD: "${DB_PASSWORD}"
    # command: mysqld --character-set-server=utf8 --collation-server=utf8_general_ci
    command: --default-authentication-plugin=mysql_native_password
    security_opt:
      - seccomp:unconfined
    expose:
      - "3306"
    volumes:
        - ./mysql:/var/lib/mysql/
    restart: always

  adminer:
    image: adminer
    restart: always
    expose:
      - "8080"

  nginx:
    image: nginx
    ports:
      - "8005:8005"
    volumes: 
      - ./nginx/conf.d/default.conf:/etc/nginx/conf.d/default.conf 
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - backend1
    restart: always
```





