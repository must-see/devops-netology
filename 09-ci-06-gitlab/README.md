# Домашнее задание к занятию "09.06 Gitlab"

## Подготовка к выполнению

1. Необходимо [подготовить gitlab к работе по инструкции](https://cloud.yandex.ru/docs/tutorials/infrastructure-management/gitlab-containers)

- Кластер k8s

![](./img/k8s.JPG)
- Реестр

![](./img/registry.JPG)
- VM с GitLab

![](./img/VM-gitlab.JPG)

- Установить через инстанс GitLab не получилось падает в ошибку

![](./img/instance_err.JPG)

2. Создайте свой новый проект
3. Создайте новый репозиторий в gitlab, наполните его [файлами](./repository)

![](./img/repository.JPG)

4. Проект должен быть публичным, остальные настройки по желанию

## Основная часть

### DevOps

В репозитории содержится код проекта на python. Проект - RESTful API сервис. Ваша задача автоматизировать сборку образа с выполнением python-скрипта:
1. Образ собирается на основе [centos:7](https://hub.docker.com/_/centos?tab=tags&page=1&ordering=last_updated)
2. Python версии не ниже 3.7
3. Установлены зависимости: `flask` `flask-restful`
4. Создана директория `/python_api`
5. Скрипт из репозитория размещён в /python_api
6. Точка вызова: запуск скрипта
7. Если сборка происходит на ветке `master`: должен подняться pod kubernetes на основе образа `python-api`, иначе этот шаг нужно пропустить

- Сборка прошла успешно

![](./img/firstBuild.JPG)

- Собранный образ в реестре

![](./img/image01.JPG)

### Product Owner

Вашему проекту нужна бизнесовая доработка: необходимо поменять JSON ответа на вызов метода GET `/rest/api/get_info`, необходимо создать Issue в котором указать:
1. Какой метод необходимо исправить
2. Текст с `{ "message": "Already started" }` на `{ "message": "Running"}`
3. Issue поставить label: feature

![](./img/Issue01.JPG)

### Developer

Вам пришел новый Issue на доработку, вам необходимо:
1. Создать отдельную ветку, связанную с этим issue
2. Внести изменения по тексту из задания
3. Подготовить Merge Requst, влить необходимые изменения в `master`, проверить, что сборка прошла успешно

![](./img/changeMethode.JPG)

![](./img/Piplines.JPG)

### Tester

Разработчики выполнили новый Issue, необходимо проверить валидность изменений:
1. Поднять докер-контейнер с образом `python-api:latest` и проверить возврат метода на корректность
2. Закрыть Issue с комментарием об успешности прохождения, указав желаемый результат и фактически достигнутый
- Загрузка образа из реестра Яндекса

![](./img/imagePull.JPG)

- Запуск образа

![](./img/dockerRun.JPG)

![](./img/getInfo.JPG)
- Закрытие задачи тестировщика

![](./img/closeIssue.JPG)

## Итог

В качестве ответа предоставьте подробные скриншоты по каждому пункту задания: файл gitlab-ci.yml, Dockerfile, лог успешного выполнения пайплайна, решенный Issue.

- [Исходный код](./source/devops-netology-main.zip)

![](./img/source.JPG)

### :bangbang: После выполнения задания выключите и удалите все задействованные ресурсы в Yandex.Cloud.

## Необязательная часть

Автомазируйте работу тестировщика, пусть у вас будет отдельный конвейер, который автоматически поднимает контейнер и выполняет проверку, например, при помощи curl. На основе вывода - будет приниматься решение об успешности прохождения тестирования

```yaml
stages:
  - build
  - deploy
  - acceptance

build:
  stage: build
  variables:
    DOCKER_DRIVER: overlay2
    DOCKER_TLS_CERTDIR: ""
    DOCKER_HOST: tcp://localhost:2375/
  image: cr.yandex/yc/metadata-token-docker-helper:0.2
  services:
    - docker:19.03.1-dind
  script:
    - docker build . -t cr.yandex/crpsrpkgfch7dn0b6937/hello:gitlab-$CI_COMMIT_SHORT_SHA
  except:
    - main  

deploy:
  stage: deploy
  variables:
    DOCKER_DRIVER: overlay2
    DOCKER_TLS_CERTDIR: ""
    DOCKER_HOST: tcp://localhost:2375/
  image: cr.yandex/yc/metadata-token-docker-helper:0.2
  services:
    - docker:19.03.1-dind
  script:
    - docker build . -t cr.yandex/crpsrpkgfch7dn0b6937/hello:gitlab-$CI_COMMIT_SHORT_SHA
    - docker push cr.yandex/crpsrpkgfch7dn0b6937/hello:gitlab-$CI_COMMIT_SHORT_SHA
  only:
    - main

curl test:
  stage: acceptance
  image: curlimages/curl 
  services:
    - name: cr.yandex/crpsrpkgfch7dn0b6937/hello:gitlab-$CI_COMMIT_SHORT_SHA
      alias: dockertest
  script:
    - curl http://dockertest:5290/get_info | grep "Running"
  only:
    - main    
```

![](./img/updPipline.JPG)

![](./img/curlOK.JPG)

+ !!! Необходимо прописать "Доступ для IP-адресов" в настройках Container Regestry Yandex'a
+ Т.к. образ качается, с Container Regestry, то он туда должен быть загружен через "docker push *", поэтому only main, тк в деплое образ не загружается в реестр