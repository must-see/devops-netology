
# Домашнее задание к занятию "11.02 Микросервисы: принципы"

Вы работаете в крупной компанию, которая строит систему на основе микросервисной архитектуры.
Вам как DevOps специалисту необходимо выдвинуть предложение по организации инфраструктуры, для разработки и эксплуатации.

## Задача 1: API Gateway 

Предложите решение для обеспечения реализации API Gateway. Составьте сравнительную таблицу возможностей различных программных решений. На основе таблицы сделайте выбор решения.

Решение должно соответствовать следующим требованиям:
- Маршрутизация запросов к нужному сервису на основе конфигурации
- Возможность проверки аутентификационной информации в запросах
- Обеспечение терминации HTTPS

Обоснуйте свой выбор.

|                                     Наименование                                     | Routing | Auth | HTTPS Termination |
|:------------------------------------------------------------------------------------:|:-------:|:----:|:-----------------:|
|                         [kong](https://github.com/Kong/kong)                         |    +    |  +   |         +         |
|                    [krakend](https://github.com/luraproject/lura)                    |    +    |  +   |         +         |
|                    [tyk](https://github.com/TykTechnologies/tyk)                     |    +    |  +   |         +         |
|                 [wso2](https://github.com/wso2/product-microgateway)                 |    +    |  +   |         +         |
|          [gravitee](https://github.com/gravitee-io/gravitee-api-management)          |    +    |  +   |         +         |
|      [Yandex API Gateway](https://cloud.yandex.ru/docs/api-gateway/quickstart/)      |    +    |  +   |         +         |
|              [Amazon API Gateway](https://aws.amazon.com/api-gateway/)               |    +    |  +   |         +         |
|  [Azure API Management](https://azure.microsoft.com/en-us/products/api-management/)  |    +    |  +   |         +         |
Если проект хостится у облачного провайдера, то лучше выбирать API Gateway этого провайдера или любой из опенсорсных с которым есть опыт работы и он имеет необходимый функционал.

[10 Top Open Source API Gateways](https://www.tecmint.com/open-source-api-gateways-and-management-tools/)

## Задача 2: Брокер сообщений

Составьте таблицу возможностей различных брокеров сообщений. На основе таблицы сделайте обоснованный выбор решения.

Решение должно соответствовать следующим требованиям:
- Поддержка кластеризации для обеспечения надежности
- Хранение сообщений на диске в процессе доставки
- Высокая скорость работы
- Поддержка различных форматов сообщений
- Разделение прав доступа к различным потокам сообщений
- Простота эксплуатации

Обоснуйте свой выбор.

Самые популярные на мой взгляд брокеры сообщений в таблице ниже, я бы выбирал основываясь на том с какими продуктами есть опыи работы и предварительно можно потестировать каждый продукт и выбрать наиболее подходяший для конкретного проекта.

| Наименование  |  Cluster |   Persistance    |  Speed | Multiformat | ACLs | Adm. overhead |
|:---:|:---:|:---:|:---:|:---:|:----:|:---:|
| [Apache kafka](https://github.com/apache/kafka) | + | + | fast | custom | + | - |
| [rabbitmq](https://github.com/rabbitmq/rabbitmq-server) | + | + | average | STOMP, AMQP, MQTT | + | + |
| [Apache ActiveMQ](https://github.com/apache/activemq) | + | + | average | OpenWire, STOMP, AMQP, MQTT, JMS | + | + |


## Задача 3: API Gateway * (необязательная)

### Есть три сервиса:

**minio**
- Хранит загруженные файлы в бакете images
- S3 протокол

**uploader**
- Принимает файл, если он картинка сжимает и загружает его в minio
- POST /v1/upload

**security**
- Регистрация пользователя POST /v1/user
- Получение информации о пользователе GET /v1/user
- Логин пользователя POST /v1/token
- Проверка токена GET /v1/token/validation

### Необходимо воспользоваться любым балансировщиком и сделать API Gateway:

**POST /v1/register**
- Анонимный доступ.
- Запрос направляется в сервис security POST /v1/user

**POST /v1/token**
- Анонимный доступ.
- Запрос направляется в сервис security POST /v1/token

**GET /v1/user**
- Проверка токена. Токен ожидается в заголовке Authorization. Токен проверяется через вызов сервиса security GET /v1/token/validation/
- Запрос направляется в сервис security GET /v1/user

**POST /v1/upload**
- Проверка токена. Токен ожидается в заголовке Authorization. Токен проверяется через вызов сервиса security GET /v1/token/validation/
- Запрос направляется в сервис uploader POST /v1/upload

**GET /v1/user/{image}**
- Проверка токена. Токен ожидается в заголовке Authorization. Токен проверяется через вызов сервиса security GET /v1/token/validation/
- Запрос направляется в сервис minio  GET /images/{image}

### Ожидаемый результат

Результатом выполнения задачи должен быть docker compose файл запустив который можно локально выполнить следующие команды с успешным результатом.
Предполагается что для реализации API Gateway будет написан конфиг для NGinx или другого балансировщика нагрузки который будет запущен как сервис через docker-compose и будет обеспечивать балансировку и проверку аутентификации входящих запросов.
Авторизаци
curl -X POST -H 'Content-Type: application/json' -d '{"login":"bob", "password":"qwe123"}' http://localhost/token

**Загрузка файла**

curl -X POST -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJib2IifQ.hiMVLmssoTsy1MqbmIoviDeFPvo-nCd92d4UFiN2O2I' -H 'Content-Type: octet/stream' --data-binary @yourfilename.jpg http://localhost/upload

**Получение файла**
curl -X GET http://localhost/images/4e6df220-295e-4231-82bc-45e4b1484430.jpg

---

#### [Дополнительные материалы: как запускать, как тестировать, как проверить](https://github.com/netology-code/devkub-homeworks/tree/main/11-microservices-02-principles)

---

### Как оформить ДЗ?

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---