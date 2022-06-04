# Домашнее задание к занятию "6.4. PostgreSQL"

## Задача 1

Используя docker поднимите инстанс PostgreSQL (версию 13). Данные БД сохраните в volume.
```commandline
docker run --rm --name postgresql \
    -e POSTGRES_PASSWORD=P@ssw0rd \
    -v data:/var/lib/postgresql/data \
    -p 5432:5432 \
    -d postgres:13
    
anton@ubuntu:~$ sudo docker ps
CONTAINER ID   IMAGE         COMMAND                  CREATED         STATUS         PORTS                                       NAMES
07f2d1f640d0   postgres:13   "docker-entrypoint.s…"   5 seconds ago   Up 4 seconds   0.0.0.0:5432->5432/tcp, :::5432->5432/tcp   postgresql
    
```
Подключитесь к БД PostgreSQL используя `psql`.
```commandline
anton@ubuntu:~$ sudo docker exec -it postgresql bash
root@07f2d1f640d0:/# psql -U postgres
psql (13.7 (Debian 13.7-1.pgdg110+1))
Type "help" for help.

postgres=# 
```

Воспользуйтесь командой `\?` для вывода подсказки по имеющимся в `psql` управляющим командам.

**Найдите и приведите** управляющие команды для:
- вывода списка БД
```commandline
postgres=# \l+
                                                                   List of databases
   Name    |  Owner   | Encoding |  Collate   |   Ctype    |   Access privileges   |  Size   | Tablespace |                Description                 
-----------+----------+----------+------------+------------+-----------------------+---------+------------+--------------------------------------------
 postgres  | postgres | UTF8     | en_US.utf8 | en_US.utf8 |                       | 7901 kB | pg_default | default administrative connection database
 template0 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +| 7753 kB | pg_default | unmodifiable empty database
           |          |          |            |            | postgres=CTc/postgres |         |            | 
 template1 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +| 7753 kB | pg_default | default template for new databases
           |          |          |            |            | postgres=CTc/postgres |         |            | 
(3 rows)
```
- подключения к БД
```commandline
postgres=# \conninfo
You are connected to database "postgres" as user "postgres" via socket in "/var/run/postgresql" at port "5432".
```
- вывода списка таблиц
```commandline
postgres=# postgres=# \dtS
                    List of relations
   Schema   |          Name           | Type  |  Owner   
------------+-------------------------+-------+----------
 pg_catalog | pg_aggregate            | table | postgres
 pg_catalog | pg_am                   | table | postgres
 pg_catalog | pg_amop                 | table | postgres
...
 pg_catalog | pg_ts_template          | table | postgres
 pg_catalog | pg_type                 | table | postgres
 pg_catalog | pg_user_mapping         | table | postgres
(62 rows)
```
- вывода описания содержимого таблиц
```commandline
postgres-# \dS+
                                            List of relations
   Schema   |              Name               | Type  |  Owner   | Persistence |    Size    | Description 
------------+---------------------------------+-------+----------+-------------+------------+-------------
 pg_catalog | pg_aggregate                    | table | postgres | permanent   | 56 kB      | 
 pg_catalog | pg_am                           | table | postgres | permanent   | 40 kB      | 
 pg_catalog | pg_amop                         | table | postgres | permanent   | 80 kB      | 
...
 pg_catalog | pg_user_mapping                 | table | postgres | permanent   | 8192 bytes | 
 pg_catalog | pg_user_mappings                | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_views                        | view  | postgres | permanent   | 0 bytes    | 
(129 rows)
```
- выхода из psql
```commandline
postgres-# \q
root@07f2d1f640d0:/# 
```

## Задача 2

Используя `psql` создайте БД `test_database`.
```commandline
root@07f2d1f640d0:/# psql -U postgres
psql (13.7 (Debian 13.7-1.pgdg110+1))
Type "help" for help.

postgres=# CREATE DATABASE test_database;
CREATE DATABASE
postgres=# 
```

Изучите [бэкап БД](https://github.com/netology-code/virt-homeworks/tree/master/06-db-04-postgresql/test_data).

Восстановите бэкап БД в `test_database`.
```commandline
anton@ubuntu:~$ sudo docker cp ./test_dump.sql postgresql:/tmp

anton@ubuntu:~$ sudo docker exec -it postgresql bash
root@07f2d1f640d0:/# psql -U postgres -f /tmp/test_dump.sql  test_database
SET
SET
SET
SET
SET
 set_config 
------------
 
(1 row)

SET
SET
SET
SET
SET
SET
CREATE TABLE
ALTER TABLE
CREATE SEQUENCE
ALTER TABLE
ALTER SEQUENCE
ALTER TABLE
COPY 8
 setval 
--------
      8
(1 row)

ALTER TABLE
```

Перейдите в управляющую консоль `psql` внутри контейнера.
```commandline
root@07f2d1f640d0:/# psql -U postgres
psql (13.7 (Debian 13.7-1.pgdg110+1))
Type "help" for help.

postgres=# 
```

Подключитесь к восстановленной БД и проведите операцию ANALYZE для сбора статистики по таблице.
```commandline
postgres=# \c test_database
You are now connected to database "test_database" as user "postgres".
test_database=# \dt
         List of relations
 Schema |  Name  | Type  |  Owner   
--------+--------+-------+----------
 public | orders | table | postgres
(1 row)

test_database=# ANALYZE VERBOSE public.orders;
INFO:  analyzing "public.orders"
INFO:  "orders": scanned 1 of 1 pages, containing 8 live rows and 0 dead rows; 8 rows in sample, 8 estimated total rows
ANALYZE
test_database=# 
```
Используя таблицу [pg_stats](https://postgrespro.ru/docs/postgresql/12/view-pg-stats), найдите столбец таблицы `orders` 
с наибольшим средним значением размера элементов в байтах.

**Приведите в ответе** команду, которую вы использовали для вычисления и полученный результат.
```commandline
test_database=# SELECT avg_width FROM pg_stats WHERE tablename='orders';
 avg_width 
-----------
         4
        16
         4
(3 rows)
```
## Задача 3

Архитектор и администратор БД выяснили, что ваша таблица orders разрослась до невиданных размеров и
поиск по ней занимает долгое время. Вам, как успешному выпускнику курсов DevOps в нетологии предложили
провести разбиение таблицы на 2 (шардировать на orders_1 - price>499 и orders_2 - price<=499).

Предложите SQL-транзакцию для проведения данной операции.
```commandline
test_database=# CREATE TABLE orders_more_499_price (CHECK (price > 499)) INHERITS (orders);
CREATE TABLE
test_database=# INSERT INTO orders_more_499_price SELECT * FROM orders WHERE price > 499;
INSERT 0 3
test_database=# CREATE TABLE orders_less_499_price (CHECK (price <= 499)) INHERITS (orders);
CREATE TABLE
test_database=# INSERT INTO orders_LESS_499_price SELECT * FROM orders WHERE price <= 499;
INSERT 0 5
test_database=# DELETE FROM ONLY orders;
DELETE 8
test_database=# \dt
                 List of relations
 Schema |         Name          | Type  |  Owner   
--------+-----------------------+-------+----------
 public | orders                | table | postgres
 public | orders_less_499_price | table | postgres
 public | orders_more_499_price | table | postgres
(3 rows)

test_database=# 
```
Можно ли было изначально исключить "ручное" разбиение при проектировании таблицы orders?
- Можно, используя декларативный подход разделения таблицы например по дате.
```commandline
CREATE TABLE measurement (
    city_id         int not null,
    logdate         date not null,
    peaktemp        int,
    unitsales       int
) PARTITION BY RANGE (logdate);

CREATE TABLE measurement_y2022m02 PARTITION OF measurement
    FOR VALUES FROM ('2022-02-01') TO ('2022-03-01');

CREATE TABLE measurement_y2022m03 PARTITION OF measurement
    FOR VALUES FROM ('2022-03-01') TO ('2022-04-01');
```

## Задача 4

Используя утилиту `pg_dump` создайте бекап БД `test_database`.
```commandline
oot@07f2d1f640d0:/# export PGPASSWORD=P@ssw0rd && pg_dump -h localhost -U postgres test_database > /tmp/test_database_backup.sql
```
Как бы вы доработали бэкап-файл, чтобы добавить уникальность значения столбца `title` для таблиц `test_database`?
```commandline
title character varying(80) NOT NULL UNIQUE
```
---

### Как cдавать задание

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---