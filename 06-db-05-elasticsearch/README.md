# Домашнее задание к занятию "6.5. Elasticsearch"

## Задача 1

В этом задании вы потренируетесь в:
- установке elasticsearch
- первоначальном конфигурировании elastcisearch
- запуске elasticsearch в docker

Используя докер образ [elasticsearch:7](https://hub.docker.com/_/elasticsearch) как базовый:

- составьте Dockerfile-манифест для elasticsearch
- соберите docker-образ и сделайте `push` в ваш docker.io репозиторий
- запустите контейнер из получившегося образа и выполните запрос пути `/` c хост-машины

Требования к `elasticsearch.yml`:
- данные `path` должны сохраняться в `/var/lib` 
- имя ноды должно быть `netology_test`

В ответе приведите:
- текст Dockerfile манифеста
```dockerfile
FROM elasticsearch:7.17.4

# container creator
MAINTAINER elasticsearch

# copy the configuration file into the container
COPY elasticsearch.yml /usr/share/elasticsearch/config


RUN chown -R elasticsearch:elasticsearch /usr/share/elasticsearch/config
RUN mkdir /var/log/elasticsearch
RUN chown -R elasticsearch:elasticsearch /var/log/elasticsearch
RUN mkdir /var/lib/elasticsearch
RUN chown -R elasticsearch:elasticsearch /var/lib/elasticsearch

# expose the default Elasticsearch port
EXPOSE 9200
```
- ссылку на образ в репозитории dockerhub
```commandline
https://hub.docker.com/repository/docker/mustsee/elasticsearch
```
- ответ `elasticsearch` на запрос пути `/` в json виде
```json
{
  "name" : "netology_test",
  "cluster_name" : "prod",
  "cluster_uuid" : "WfHaLZEGR4GeSnZfsBjWHA",
  "version" : {
    "number" : "7.17.4",
    "build_flavor" : "default",
    "build_type" : "docker",
    "build_hash" : "79878662c54c886ae89206c685d9f1051a9d6411",
    "build_date" : "2022-05-18T18:04:20.964345128Z",
    "build_snapshot" : false,
    "lucene_version" : "8.11.1",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}
```

Подсказки:
- при сетевых проблемах внимательно изучите кластерные и сетевые настройки в elasticsearch.yml
- при некоторых проблемах вам поможет docker директива ulimit
- elasticsearch в логах обычно описывает проблему и пути ее решения
- обратите внимание на настройки безопасности такие как `xpack.security.enabled` 
- если докер образ не запускается и падает с ошибкой 137 в этом случае может помочь настройка `-e ES_HEAP_SIZE`
- при настройке `path` возможно потребуется настройка прав доступа на директорию

Далее мы будем работать с данным экземпляром elasticsearch.

## Задача 2

В этом задании вы научитесь:
- создавать и удалять индексы
- изучать состояние кластера
- обосновывать причину деградации доступности данных

Ознакомтесь с [документацией](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-create-index.html) 
и добавьте в `elasticsearch` 3 индекса, в соответствии со таблицей:

| Имя | Количество реплик | Количество шард |
|-----|-------------------|-----------------|
| ind-1| 0 | 1 |
| ind-2 | 1 | 2 |
| ind-3 | 2 | 4 |

```commandline
anton@ubuntu:~$ curl -X PUT "localhost:9200/ind-1?pretty" -H 'Content-Type: application/json' -d'
> {
>   "settings": {
>     "number_of_shards": 1,
>     "number_of_replicas": 0
>   }
> }
> '
{
  "acknowledged" : true,
  "shards_acknowledged" : true,
  "index" : "ind-1"
}
```

```commandline
anton@ubuntu:~$ curl -X PUT "localhost:9200/ind-2?pretty" -H 'Content-Type: application/json' -d'
> {
>   "settings": {
>     "number_of_shards": 2,
>     "number_of_replicas": 1
>   }
> }
> '
{
  "acknowledged" : true,
  "shards_acknowledged" : true,
  "index" : "ind-2"
}
```
```commandline
anton@ubuntu:~$ curl -X PUT "localhost:9200/ind-3?pretty" -H 'Content-Type: application/json' -d'
> {
>   "settings": {
>     "number_of_shards": 4,
>     "number_of_replicas": 2
>   }
> }
> '
{
  "acknowledged" : true,
  "shards_acknowledged" : true,
  "index" : "ind-3"
}
```

Получите список индексов и их статусов, используя API и **приведите в ответе** на задание.
```commandline
anton@ubuntu:~$ curl 'localhost:9200/_cat/indices?v'
health status index            uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   .geoip_databases yaVmptSKT4G3TTqtLmV5eQ   1   0         40            0     38.2mb         38.2mb
green  open   ind-1            VuUqruMlRp-QFt7S2Num2A   1   0          0            0       226b           226b
yellow open   ind-3            K8CUUprTTWSiMkgPF_Bm9g   4   2          0            0       904b           904b
yellow open   ind-2            1KoD_cEEQM6V-ZaxjyR68w   2   1          0            0       452b           452b
```
Получите состояние кластера `elasticsearch`, используя API.
```commandline
anton@ubuntu:~$ curl -X GET "localhost:9200/_cluster/health?pretty"
{
  "cluster_name" : "prod",
  "status" : "yellow",
  "timed_out" : false,
  "number_of_nodes" : 1,
  "number_of_data_nodes" : 1,
  "active_primary_shards" : 10,
  "active_shards" : 10,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 10,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 50.0
}
```
Как вы думаете, почему часть индексов и кластер находится в состоянии yellow?
```commandline
В состоянии yellow тк не возможно обеспечить отказоустойчивость в рамках одного хоста.
```
Удалите все индексы.
```commandline
anton@ubuntu:~$ curl -X DELETE 'http://localhost:9200/_all'
{"acknowledged":true}
```
**Важно**

При проектировании кластера elasticsearch нужно корректно рассчитывать количество реплик и шард,
иначе возможна потеря данных индексов, вплоть до полной, при деградации системы.

## Задача 3

В данном задании вы научитесь:
- создавать бэкапы данных
- восстанавливать индексы из бэкапов

Создайте директорию `{путь до корневой директории с elasticsearch в образе}/snapshots`.
```dockerfile
FROM elasticsearch:7.17.4

# container creator
MAINTAINER elasticsearch

# copy the configuration file into the container
COPY elasticsearch.yml /usr/share/elasticsearch/config


RUN chown -R elasticsearch:elasticsearch /usr/share/elasticsearch/config 
RUN mkdir /var/log/elasticsearch
RUN chown -R elasticsearch:elasticsearch /var/log/elasticsearch
RUN mkdir /var/lib/elasticsearch
RUN chown -R elasticsearch:elasticsearch /var/lib/elasticsearch
RUN mkdir /var/lib/elasticsearch/snapshots
RUN chown -R elasticsearch:elasticsearch /var/lib/elasticsearch/snapshots

# expose the default Elasticsearch port
EXPOSE 9200
```

```yaml
path:
    data: /var/lib/elasticsearch
    logs: /var/log/elasticsearch
    repo: /var/lib/elasticsearch/snapshots
    
cluster.name: "prod"
node.name: "netology_test"
network.host: 0.0.0.0
```
Используя API [зарегистрируйте](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-register-repository.html#snapshots-register-repository) 
данную директорию как `snapshot repository` c именем `netology_backup`.
```commandline
anton@ubuntu:~$ curl -X PUT "localhost:9200/_snapshot/netology_backup?pretty" -H 'Content-Type: application/json' -d'
> {
>   "type": "fs",
>   "settings": {
>     "location": "/var/lib/elasticsearch/snapshots",
>     "compress": true
>   }
> }'
{
  "acknowledged" : true
}
```
**Приведите в ответе** запрос API и результат вызова API для создания репозитория.

Создайте индекс `test` с 0 реплик и 1 шардом и **приведите в ответе** список индексов.
```commandline
anton@ubuntu:~$ curl -X PUT "localhost:9200/test?pretty" -H 'Content-Type: application/json' -d'
> {
>   "settings": {
>     "number_of_shards": 1,
>     "number_of_replicas": 0
>   }
> }
> '
{
  "acknowledged" : true,
  "shards_acknowledged" : true,
  "index" : "test"
}
anton@ubuntu:~$ curl 'localhost:9200/_cat/indices?v'
health status index            uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   .geoip_databases jp3Cfj9lQ0-VTkNwNrTOQA   1   0         40            0     38.2mb         38.2mb
green  open   test             Ao-sZaVpQB6AnPBpJNLFUw   1   0          0            0       226b           226b
```
[Создайте `snapshot`](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-take-snapshot.html) 
состояния кластера `elasticsearch`.
```commandline
anton@ubuntu:~$ curl -X PUT "localhost:9200/_snapshot/netology_backup/snapshot01?wait_for_completion=true&pretty"
```
**Приведите в ответе** список файлов в директории со `snapshot`ами.
```commandline
sh-5.0# ls -la /var/lib/elasticsearch/snapshots/
total 40
drwxr-xr-x 1 elasticsearch elasticsearch 4096 Jun  5 11:01 .
drwxr-xr-x 1 elasticsearch elasticsearch 4096 Jun  5 10:55 ..
-rw-rw-r-- 1 elasticsearch root          1422 Jun  5 11:01 index-0
-rw-rw-r-- 1 elasticsearch root             8 Jun  5 11:01 index.latest
drwxrwxr-x 6 elasticsearch root          4096 Jun  5 11:01 indices
-rw-rw-r-- 1 elasticsearch root          9767 Jun  5 11:01 meta-zbU8dpQVTMa6T3onXx1eTg.dat
-rw-rw-r-- 1 elasticsearch root           455 Jun  5 11:01 snap-zbU8dpQVTMa6T3onXx1eTg.dat
```
Удалите индекс `test` и создайте индекс `test-2`. **Приведите в ответе** список индексов.
```commandline
anton@ubuntu:~$ curl -X DELETE "localhost:9200/test?pretty"
{
  "acknowledged" : true
}
anton@ubuntu:~$ curl -X PUT "localhost:9200/test-2?pretty" -H 'Content-Type: application/json' -d'
> {
>   "settings": {
>     "number_of_shards": 1,
>     "number_of_replicas": 0
>   }
> }
> '
{
  "acknowledged" : true,
  "shards_acknowledged" : true,
  "index" : "test-2"
}
anton@ubuntu:~$ curl 'localhost:9200/_cat/indices?pretty'
green open test-2           goUtBHrWScCBc-c9Tb9E-A 1 0  0 0   226b   226b
green open .geoip_databases jp3Cfj9lQ0-VTkNwNrTOQA 1 0 40 0 38.2mb 38.2mb
```
[Восстановите](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-restore-snapshot.html) состояние
кластера `elasticsearch` из `snapshot`, созданного ранее. 

**Приведите в ответе** запрос к API восстановления и итоговый список индексов.
```commandline
curl -X POST "localhost:9200/_snapshot/netology_backup/snapshot01/_restore?pretty" -H 'Content-Type: application/json' -d'
{
  "indices": "*",
  "include_global_state": true
}
'
```
При выполнении ошибка вида:
```commandline
anton@ubuntu:~$ curl -X POST "localhost:9200/_snapshot/netology_backup/snapshot01/_restore?pretty" -H 'Content-Type: application/json' -d'
{
  "indices": "*",
  "include_global_state": true
}
'
{
  "error" : {
    "root_cause" : [
      {
        "type" : "snapshot_restore_exception",
        "reason" : "[netology_backup:snapshot01/zbU8dpQVTMa6T3onXx1eTg] cannot restore index [.ds-ilm-history-5-2022.06.05-000001] because an open index with same name already exists in the cluster. Either close or delete the existing index or restore the index under a different name by providing a rename pattern and replacement name"
      }
    ],
    "type" : "snapshot_restore_exception",
    "reason" : "[netology_backup:snapshot01/zbU8dpQVTMa6T3onXx1eTg] cannot restore index [.ds-ilm-history-5-2022.06.05-000001] because an open index with same name already exists in the cluster. Either close or delete the existing index or restore the index under a different name by providing a rename pattern and replacement name"
  },
  "status" : 500
}
```
Закрываем индексы:
```commandline
curl -X POST "localhost:9200/.ds-.logs-deprecation.elasticsearch-default-2022.06.05-000001/_close?pretty"
curl -X POST "localhost:9200/.ds-ilm-history-5-2022.06.05-000001/_close?pretty"
```
После этого успешно проходит восстановление.
```commandline
anton@ubuntu:~$ curl -X POST "localhost:9200/_snapshot/netology_backup/snapshot01/_restore?pretty" -H 'Content-Type: application/json' -d'
{
  "indices": "*",
  "include_global_state": true
}
'
{
  "accepted" : true
}
anton@ubuntu:~$ curl 'localhost:9200/_cat/indices?pretty'
green open test-2           goUtBHrWScCBc-c9Tb9E-A 1 0  0 0   226b   226b
green open .geoip_databases ityLF1ksQx2c0u_sGDYYpw 1 0 40 0 38.2mb 38.2mb
green open test             rOiBhYyhS2uxQshKYDXT8w 1 0  0 0   226b   226b
```
Образ с настроенной директорией для snap https://hub.docker.com/repository/docker/mustsee/elasticsearchsnap

Подсказки:
- возможно вам понадобится доработать `elasticsearch.yml` в части директивы `path.repo` и перезапустить `elasticsearch`

---

### Как cдавать задание

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---