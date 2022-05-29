# Домашнее задание к занятию "6.2. SQL"

## Введение

Перед выполнением задания вы можете ознакомиться с 
[дополнительными материалами](https://github.com/netology-code/virt-homeworks/tree/master/additional/README.md).

## Задача 1

Используя docker поднимите инстанс PostgreSQL (версию 12) c 2 volume, 
в который будут складываться данные БД и бэкапы.

Приведите получившуюся команду или docker-compose манифест.
```dockerfile
version: '3.6'

volumes:
  data: {}
  backup: {}

services:

  postgres:
    image: postgres:12
    container_name: psg
    ports:
      - "0.0.0.0:5432:5432"
    volumes:
      - data:/var/lib/postgresql/data
      - backup:/media/postgresql/backup
    environment:
      POSTGRES_USER: "admin-user"
      POSTGRES_PASSWORD: "P@ssw0rd"
      POSTGRES_DB: "psg_db"
    restart: always
```

```commandline
sudo docker compose up -d

sudo docker compose ls
NAME                STATUS              CONFIG FILES
62sql               running(1)          /home/anton/Desktop/6.2SQL/docker-compose.yml

sudo docker exec -it psg bash

export PGPASSWORD="P@ssw0rd" && psql -h localhost -U admin-user psg_db
psql (12.11 (Debian 12.11-1.pgdg110+1))
Type "help" for help.
```
## Задача 2

В БД из задачи 1: 
- создайте пользователя test-admin-user и БД test_db
- в БД test_db создайте таблицу orders и clients (спeцификация таблиц ниже)
- предоставьте привилегии на все операции пользователю test-admin-user на таблицы БД test_db
- создайте пользователя test-simple-user  
- предоставьте пользователю test-simple-user права на SELECT/INSERT/UPDATE/DELETE данных таблиц БД test_db

Таблица orders:
- id (serial primary key)
- наименование (string)
- цена (integer)

Таблица clients:
- id (serial primary key)
- фамилия (string)
- страна проживания (string, index)
- заказ (foreign key orders)

Приведите:
- итоговый список БД после выполнения пунктов выше,
- описание таблиц (describe)
- SQL-запрос для выдачи списка пользователей с правами над таблицами test_db
- список пользователей с правами над таблицами test_db

```commandline
CREATE USER "test-admin-user" WITH PASSWORD 'P@ssw0rd';

CREATE DATABASE test_db;

CREATE TABLE orders (
    id SERIAL,
    наименование VARCHAR, 
    цена INTEGER,
    PRIMARY KEY (id)
);

CREATE TABLE clients (
    id SERIAL,
    фамилия VARCHAR,
    "страна проживания" VARCHAR, 
    заказ INTEGER,
    PRIMARY KEY (id),
    CONSTRAINT fk_заказ
      FOREIGN KEY(заказ) 
	    REFERENCES orders(id)
);

CREATE INDEX ON clients("страна проживания");

GRANT ALL ON TABLE orders, clients TO "test-admin-user";

CREATE USER "test-simple-user" WITH PASSWORD 'P@ssw0rd';

GRANT SELECT, INSERT, UPDATE, DELETE ON orders, clients TO "test-simple-user";
```
итоговый список БД после выполнения пунктов выше
```commandline
test_db=# \l+
                                                                        List of databases
   Name    |   Owner    | Encoding |  Collate   |   Ctype    |       Access privileges       |  Size   | Tablespace |                Description                 
-----------+------------+----------+------------+------------+-------------------------------+---------+------------+--------------------------------------------
 postgres  | admin-user | UTF8     | en_US.utf8 | en_US.utf8 |                               | 7969 kB | pg_default | default administrative connection database
 psg_db    | admin-user | UTF8     | en_US.utf8 | en_US.utf8 |                               | 8113 kB | pg_default | 
 template0 | admin-user | UTF8     | en_US.utf8 | en_US.utf8 | =c/"admin-user"              +| 7825 kB | pg_default | unmodifiable empty database
           |            |          |            |            | "admin-user"=CTc/"admin-user" |         |            | 
 template1 | admin-user | UTF8     | en_US.utf8 | en_US.utf8 | =c/"admin-user"              +| 7825 kB | pg_default | default template for new databases
           |            |          |            |            | "admin-user"=CTc/"admin-user" |         |            | 
 test_db   | admin-user | UTF8     | en_US.utf8 | en_US.utf8 |                               | 7825 kB | pg_default | 
(5 rows)
```
описание таблиц (describe)
```commandline
test_db=# \d+ clients
                                                           Table "public.clients"
      Column       |       Type        | Collation | Nullable |               Default               | Storage  | Stats target | Description 
-------------------+-------------------+-----------+----------+-------------------------------------+----------+--------------+-------------
 id                | integer           |           | not null | nextval('clients_id_seq'::regclass) | plain    |              | 
 фамилия           | character varying |           |          |                                     | extended |              | 
 страна проживания | character varying |           |          |                                     | extended |              | 
 заказ             | integer           |           |          |                                     | plain    |              | 
Indexes:
    "clients_pkey" PRIMARY KEY, btree (id)
    "clients_страна проживания_idx" btree ("страна проживания")
Foreign-key constraints:
    "fk_заказ" FOREIGN KEY ("заказ") REFERENCES orders(id)
Access method: heap

sg_db=# \d+ orders
                                                        Table "public.orders"
    Column    |       Type        | Collation | Nullable |              Default               | Storage  | Stats target | Description 
--------------+-------------------+-----------+----------+------------------------------------+----------+--------------+-------------
 id           | integer           |           | not null | nextval('orders_id_seq'::regclass) | plain    |              | 
 наименование | character varying |           |          |                                    | extended |              | 
 цена         | integer           |           |          |                                    | plain    |              | 
Indexes:
    "orders_pkey" PRIMARY KEY, btree (id)
Referenced by:
    TABLE "clients" CONSTRAINT "fk_заказ" FOREIGN KEY ("заказ") REFERENCES orders(id)
Access method: heap
```
SQL-запрос для выдачи списка пользователей с правами над таблицами test_db
```commandline
test_db=# SELECT 
    grantee, table_name, privilege_type 
FROM 
    information_schema.table_privileges 
WHERE 
    grantee in ('test-admin-user','test-simple-user')
    and table_name in ('clients','orders')
order by 
    1,2,3;
     grantee      | table_name | privilege_type 
------------------+------------+----------------
 test-admin-user  | clients    | DELETE
 test-admin-user  | clients    | INSERT
 test-admin-user  | clients    | REFERENCES
 test-admin-user  | clients    | SELECT
 test-admin-user  | clients    | TRIGGER
 test-admin-user  | clients    | TRUNCATE
 test-admin-user  | clients    | UPDATE
 test-admin-user  | orders     | DELETE
 test-admin-user  | orders     | INSERT
 test-admin-user  | orders     | REFERENCES
 test-admin-user  | orders     | SELECT
 test-admin-user  | orders     | TRIGGER
 test-admin-user  | orders     | TRUNCATE
 test-admin-user  | orders     | UPDATE
 test-simple-user | clients    | DELETE
 test-simple-user | clients    | INSERT
 test-simple-user | clients    | SELECT
 test-simple-user | clients    | UPDATE
 test-simple-user | orders     | DELETE
 test-simple-user | orders     | INSERT
 test-simple-user | orders     | SELECT
 test-simple-user | orders     | UPDATE
(22 rows)

```
## Задача 3

Используя SQL синтаксис - наполните таблицы следующими тестовыми данными:

Таблица orders

|Наименование|цена|
|------------|----|
|Шоколад| 10 |
|Принтер| 3000 |
|Книга| 500 |
|Монитор| 7000|
|Гитара| 4000|

Таблица clients

|ФИО|Страна проживания|
|------------|----|
|Иванов Иван Иванович| USA |
|Петров Петр Петрович| Canada |
|Иоганн Себастьян Бах| Japan |
|Ронни Джеймс Дио| Russia|
|Ritchie Blackmore| Russia|

Используя SQL синтаксис:
- вычислите количество записей для каждой таблицы 
- приведите в ответе:
    - запросы 
    - результаты их выполнения.

```commandline
INSERT INTO orders VALUES (1, 'Шоколад', 10), (2, 'Принтер', 3000), (3, 'Книга', 500), (4, 'Монитор', 7000), (5, 'Гитара', 4000);
INSERT 0 5

test_db=# SELECT count(1) FROM orders;
 count 
-------
     5
(1 row)

test_db=# INSERT INTO clients VALUES (1, 'Иванов Иван Иванович', 'USA'), (2, 'Петров Петр Петрович', 'Canada'), (3, 'Иоганн Себастьян Бах', 'Japan'), (4, 'Ронни Джеймс Дио', 'Russia'), (5, 'Ritchie Blackmore', 'Russia');
INSERT 0 5
psg_db=# SELECT count(1) FROM clients;
 count 
-------
     5
(1 row)

```

## Задача 4

Часть пользователей из таблицы clients решили оформить заказы из таблицы orders.

Используя foreign keys свяжите записи из таблиц, согласно таблице:

|ФИО|Заказ|
|------------|----|
|Иванов Иван Иванович| Книга |
|Петров Петр Петрович| Монитор |
|Иоганн Себастьян Бах| Гитара |

Приведите SQL-запросы для выполнения данных операций.

Приведите SQL-запрос для выдачи всех пользователей, которые совершили заказ, а также вывод данного запроса.
 
Подсказка - используйте директиву `UPDATE`.

```commandline
test_db=# UPDATE clients SET "заказ" = (SELECT id FROM orders WHERE "наименование"='Книга') WHERE "фамилия"='Иванов Иван Иванович';
UPDATE 1

test_db=# UPDATE clients SET "заказ" = (SELECT id FROM orders WHERE "наименование"='Монитор') WHERE "фамилия"='Петров Петр Петрович';
UPDATE 1

test_db=# UPDATE clients SET "заказ" = (SELECT id FROM orders WHERE "наименование"='Гитара') WHERE "фамилия"='Иоганн Себастьян Бах';
UPDATE 1

test_db=# SELECT c.* FROM clients c JOIN orders o ON c.заказ = o.id;
 id |       фамилия        | страна проживания | заказ 
----+----------------------+-------------------+-------
  1 | Иванов Иван Иванович | USA               |     3
  2 | Петров Петр Петрович | Canada            |     4
  3 | Иоганн Себастьян Бах | Japan             |     5
(3 rows)
```

## Задача 5

Получите полную информацию по выполнению запроса выдачи всех пользователей из задачи 4 
(используя директиву EXPLAIN).

Приведите получившийся результат и объясните что значат полученные значения.
```commandline
test_db=# EXPLAIN SELECT c.* FROM clients c JOIN orders o ON c.заказ = o.id;
                               QUERY PLAN                               
------------------------------------------------------------------------
 Hash Join  (cost=37.00..57.24 rows=810 width=72)
   Hash Cond: (c."заказ" = o.id)
   ->  Seq Scan on clients c  (cost=0.00..18.10 rows=810 width=72)
   ->  Hash  (cost=22.00..22.00 rows=1200 width=4)
         ->  Seq Scan on orders o  (cost=0.00..22.00 rows=1200 width=4)
(5 rows)
```
Здесь планировщик выбирает соединение по хешу, при котором строки одной таблицы записываются в хеш-таблицу в памяти, после чего сканируется другая таблица и для каждой её строки проверяется соответствие по хеш-таблице.
Seq Scan (Последовательное сканирование). Это означает, что узел плана проверяет это условие для каждого просканированного им узла и выводит только те строки, которые удовлетворяют ему.

## Задача 6

Создайте бэкап БД test_db и поместите его в volume, предназначенный для бэкапов (см. Задачу 1).

Остановите контейнер с PostgreSQL (но не удаляйте volumes).

Поднимите новый пустой контейнер с PostgreSQL.

Восстановите БД test_db в новом контейнере.

Приведите список операций, который вы применяли для бэкапа данных и восстановления. 

```commandline
export PGPASSWORD=P@ssw0rd && pg_dumpall -h localhost -U admin-user > /media/postgresql/backup/test_db.sql

sudo docker compose stop

sudo docker volume ls
DRIVER    VOLUME NAME
local     62sql_backup
local     62sql_data

docker run --rm -d -e POSTGRES_USER=admin-user -e POSTGRES_PASSWORD=P@ssw0rd -e POSTGRES_DB=test_db -v 62sql_backup:/media/postgresql/backup --name psql2 postgres:12

udo docker ps -a
CONTAINER ID   IMAGE                           COMMAND                  CREATED          STATUS                      PORTS      NAMES
e6fb64b620b6   postgres:12                     "docker-entrypoint.s…"   23 seconds ago   Up 22 seconds               5432/tcp   psql2
038a22924756   postgres:12                     "docker-entrypoint.s…"   2 hours ago      Exited (0) 22 minutes ago              psg

sudo docker exec -it psql2  bash

root@e6fb64b620b6:/# ls /media/postgresql/backup/
test_db.sql

root@e6fb64b620b6:/# export PGPASSWORD=P@ssw0rd && psql -h localhost -U admin-user -f /media/postgresql/backup/test_db.sql test_db

```

---

### Как cдавать задание

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---