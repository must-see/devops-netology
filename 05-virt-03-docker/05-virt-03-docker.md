## Задача 1

Сценарий выполнения задачи:

- создайте свой репозиторий на https://hub.docker.com;
- выберете любой образ, который содержит веб-сервер Nginx;
- создайте свой fork образа;
- реализуйте функциональность:
запуск веб-сервера в фоне с индекс-страницей, содержащей HTML-код ниже:
```
<html>
<head>
Hey, Netology
</head>
<body>
<h1>I’m DevOps Engineer!</h1>
</body>
</html>
```
Опубликуйте созданный форк в своем репозитории и предоставьте ответ в виде ссылки на https://hub.docker.com/username_repo.
```
docker pull nginx:1.21
1.21: Pulling from library/nginx
Digest: sha256:859ab6768a6f26a79bc42b231664111317d095a4f04e4b6fe79ce37b3d199097
Status: Downloaded newer image for nginx:1.21

sudo docker build -t mustsee/nginx-devops:1.21 .
Sending build context to Docker daemon  3.072kB
Step 1/3 : FROM nginx:1.21
 ---> fa5269854a5e
Step 2/3 : COPY index.html /usr/share/nginx/html/
 ---> 179c85971def
Step 3/3 : RUN chown nginx:nginx /usr/share/nginx/html/*
 ---> Running in b913ef882bfa
Removing intermediate container b913ef882bfa
 ---> 5a5e597c3080
Successfully built 5a5e597c3080
Successfully tagged mustsee/nginx-devops:1.21

sudo docker run -d --rm  -p 80:80 mustsee/nginx-devops:1.21
3fd82e8823ecf727e6ebd435cb0b2165b5718a6dac73e3060bf5e9b583a37c52

sudo docker login

sudo docker push mustsee/nginx-devops:1.21
The push refers to repository [docker.io/mustsee/nginx-devops]
123e13980a6c: Pushed 
7c5efa3865f4: Pushed 
b6812e8d56d6: Mounted from library/nginx 
7046505147d7: Mounted from library/nginx 
c876aa251c80: Mounted from library/nginx 
f5ab86d69014: Mounted from library/nginx 
4b7fffa0f0a4: Mounted from library/nginx 
9c1b6dd6c1e6: Mounted from library/nginx 
1.21: digest: sha256:98025700ed53428d441267eb8423a03182b671d12a2ea8ea5930a0377ea3155d size: 1984

sudo docker stop 3fd82e8823ec
sudo docker image rm 5a5e597c3080

sudo docker pull mustsee/nginx-devops:1.21
1.21: Pulling from mustsee/nginx-devops
1fe172e4850f: Already exists 
35c195f487df: Already exists 
213b9b16f495: Already exists 
a8172d9e19b9: Already exists 
f5eee2cb2150: Already exists 
93e404ba8667: Already exists 
b456a0d3efa4: Pull complete 
0c7021e6acf9: Pull complete 
Digest: sha256:98025700ed53428d441267eb8423a03182b671d12a2ea8ea5930a0377ea3155d
Status: Downloaded newer image for mustsee/nginx-devops:1.21
docker.io/mustsee/nginx-devops:1.21

sudo docker run -d --rm  -p 80:80 mustsee/nginx-devops:1.21
a441ef01a4ab7c3dfd8e92afa3bcf16d3f66456b1e5d9132fffd03b207b736db

sudo docker ps
CONTAINER ID   IMAGE                       COMMAND                  CREATED          STATUS          PORTS                               NAMES
a441ef01a4ab   mustsee/nginx-devops:1.21   "/docker-entrypoint.…"   46 seconds ago   Up 45 seconds   0.0.0.0:80->80/tcp, :::80->80/tcp   sad_keller

https://hub.docker.com/repository/docker/mustsee/nginx-devops

```


## Задача 2

Посмотрите на сценарий ниже и ответьте на вопрос:
"Подходит ли в этом сценарии использование Docker контейнеров или лучше подойдет виртуальная машина, физическая машина? Может быть возможны разные варианты?"

Детально опишите и обоснуйте свой выбор.

--

Сценарий:

- Высоконагруженное монолитное java веб-приложение;
  Виртуальные или физ. сервера, docker создавался чтобы уйти от монолита.
  
- Nodejs веб-приложение;
  Docker подойдет т.к. приложение легковесно и можно легко масштабировать.

- Мобильное приложение c версиями для Android и iOS;
  Если речь про веб версию мобильного приложения или API, то docker подойдет. 
  
- Шина данных на базе Apache Kafka;
  Для не очень нагруженных инсталляций думаю можно использовать и Docker
  
- Elasticsearch кластер для реализации логирования продуктивного веб-приложения - три ноды elasticsearch, два logstash и две ноды kibana;
  Если предполагается большой объем данных и высокая нагрузка, то лучше использовать виртуальные или физ. сервера.
  
- Мониторинг-стек на базе Prometheus и Grafana;
  Docker подходит тк легко и быстро можно масштабироваться

- MongoDB, как основное хранилище данных для java-приложения;
  Лучше использовать виртуальные или физ. сервера для СУБД тк лучше организовано хранение данных и бэкап

- Gitlab сервер для реализации CI/CD процессов и приватный (закрытый) Docker Registry.
  Для больших инсталляций лучше использовать виртуальные или физ. сервера тк лучше организовано хранение данных и бэкап

## Задача 3

- Запустите первый контейнер из образа ***centos*** c любым тэгом в фоновом режиме, подключив папку ```/data``` из текущей рабочей директории на хостовой машине в ```/data``` контейнера;
```commandline
docker run -v /data:/data -dt --name centos centos
Unable to find image 'centos:latest' locally
latest: Pulling from library/centos
a1d0c7532777: Pull complete 
Digest: sha256:a27fd8080b517143cbbbab9dfb7c8571c40d67d534bbdee55bd6c473f432b177
Status: Downloaded newer image for centos:latest
766f0ffc515ab7bce5d16241b2b0826766e3ea561739a4e972f8a01ce2a74d0b
```
- Запустите второй контейнер из образа ***debian*** в фоновом режиме, подключив папку ```/data``` из текущей рабочей директории на хостовой машине в ```/data``` контейнера;
```commandline
docker run -v /data:/data -dt --name debian debian
Unable to find image 'debian:latest' locally
latest: Pulling from library/debian
6aefca2dc61d: Pull complete 
Digest: sha256:6846593d7d8613e5dcc68c8f7d8b8e3179c7f3397b84a47c5b2ce989ef1075a0
Status: Downloaded newer image for debian:latest
4ebafe6f0963a6f8c6ef5b5fe8c95f9f53e1adbc8d55284bbba8fdce990a9ed6
```
- Подключитесь к первому контейнеру с помощью ```docker exec``` и создайте текстовый файл любого содержания в ```/data```;
```commandline
docker exec -it centos /bin/sh
sh-4.4# echo 'centos'>/data/centos
sh-4.4# exit
exit

```
- Добавьте еще один файл в папку ```/data``` на хостовой машине;
```commandline
echo 'localhost'>/data/localhost
```
- Подключитесь во второй контейнер и отобразите листинг и содержание файлов в ```/data``` контейнера.
```commandline
ocker exec -it debian /bin/sh
# ls -la /data
total 16
drwxr-xr-x 2 root root 4096 Apr 23 20:16 .
drwxr-xr-x 1 root root 4096 Apr 23 20:09 ..
-rw-r--r-- 1 root root    7 Apr 23 20:11 centos
-rw-r--r-- 1 root root   10 Apr 23 20:16 localhost


# cd /data
# cat centos
centos
# cat localhost
localhost

```

## Задача 4 (*)

Воспроизвести практическую часть лекции самостоятельно.

Соберите Docker образ с Ansible, загрузите на Docker Hub и пришлите ссылку вместе с остальными ответами к задачам.

```commandline
sudo docker build -t mustsee/alpine-ansible:2.10.0 .

ending build context to Docker daemon  3.072kB
Step 1/5 : FROM alpine:3.14
 ---> e04c818066af
Step 2/5 : RUN CARGO_NET_GIT_FETCH_WITH_CLI=1 &&     apk --no-cache add         sudo         python3        py3-pip         openssl         ca-certificates         sshpass         openssh-client         rsync         git &&     apk --no-cache add --virtual build-dependencies         python3-dev         libffi-dev         musl-dev         gcc         cargo         openssl-dev         libressl-dev         build-base &&     pip install --upgrade pip wheel &&     pip install --upgrade cryptography cffi &&     pip uninstall ansible-base &&     pip install ansible-core &&     pip install ansible==2.10.0 &&     pip install mitogen ansible-lint jmespath &&     pip install --upgrade pywinrm &&     apk del build-dependencies &&     rm -rf /var/cache/apk/* &&     rm -rf /root/.cache/pip &&     rm -rf /root/.cargo
 ---> Running in 2840ae4f5043
fetch https://dl-cdn.alpinelinux.org/alpine/v3.14/main/x86_64/APKINDEX.tar.gz
fetch https://dl-cdn.alpinelinux.org/alpine/v3.14/community/x86_64/APKINDEX.tar.gz
(1/55) Installing ca-certificates (20211220-r0)
(2/55) Installing brotli-libs (1.0.9-r5)
(3/55) Installing nghttp2-libs (1.43.0-r0)
(4/55) Installing libcurl (7.79.1-r0)

...

(37/37) Purging libmagic (5.40-r1)
Executing busybox-1.33.1-r7.trigger
OK: 98 MiB in 69 packages
Removing intermediate container 2840ae4f5043
 ---> eaf9c42154d7
Step 3/5 : RUN mkdir /ansible &&     mkdir -p /etc/ansible &&     echo 'localhost' > /etc/ansible/hosts
 ---> Running in 1267218324a8
Removing intermediate container 1267218324a8
 ---> ca78450f78e9
Step 4/5 : WORKDIR /ansible
 ---> Running in 7e7c96d2c7a7
Removing intermediate container 7e7c96d2c7a7
 ---> f4d052bcc509
Step 5/5 : CMD [ "ansible-playbook", "--version" ]
 ---> Running in 3069b8466c95
Removing intermediate container 3069b8466c95
 ---> 07aaf71b892f
Successfully built 07aaf71b892f
Successfully tagged mustsee/alpine-ansible:2.10.0

```
```commandline
sudo docker images
REPOSITORY               TAG       IMAGE ID       CREATED          SIZE
mustsee/alpine-ansible   2.10.0    07aaf71b892f   29 seconds ago   371MB

```

https://hub.docker.com/repository/docker/mustsee/alpine-ansible
