### Домашнее задание к занятию "4.3. Языки разметки JSON и YAML"


#### Обязательная задача 1
Мы выгрузили JSON, который получили через API запрос к нашему сервису:
```
    { "info" : "Sample JSON output from our service\t",
        "elements" :[
            { "name" : "first",
            "type" : "server",
            "ip" : 7175 
            }
            { "name" : "second",
            "type" : "proxy",
            "ip : 71.78.22.43
            }
        ]
    }
```
  Нужно найти и исправить все ошибки, которые допускает наш сервис

- 2 строка - пропущен пробел между `:` и `[` (открытие массива)
- 1,3,7 строки - после скобки `{` сделать перенос (для улучшения читаемости)
- 5 строка - неверная запись ip адреса, не дописан и без кавычек
- 9 строка - пропущены закрывающиеся кавычки `ip"` и кавычки на значении
- 

```json
{
 "info" : "Sample JSON output from our service\t",
  "elements" : [
    {
     "name" : "first",
     "type" : "server",
     "ip" : "71.75.22.42" 
    },
    {
     "name" : "second",
     "type" : "proxy",
     "ip" : "71.78.22.43"
    }
  ]
}
```


#### Обязательная задача 2
В прошлый рабочий день мы создавали скрипт, позволяющий опрашивать веб-сервисы и получать их IP. К уже реализованному функционалу нам нужно добавить возможность записи JSON и YAML файлов, описывающих наши сервисы. Формат записи JSON по одному сервису: `{ "имя сервиса" : "его IP"}`. Формат записи YAML по одному сервису: `- имя сервиса: его IP`. Если в момент исполнения скрипта меняется IP у сервиса - он должен так же поменяться в yml и json файле.

#### Ваш скрипт:
```python
# !/usr/bin/env python3

import os
import json
import yaml
import time
import socket


site_list = ['drive.google.com', 'mail.google.com', 'google.com']
site_dict = {}

def check_list_of_sites(site_list, site_dict):

    for site_url in site_list:
        site_dict = check_site_dns(site_url, site_dict)
    return site_dict


def check_site_dns(site_url, site_dict):
    site_new_ip = []

    result_os = socket.gethostbyname(site_url)
    site_new_ip.append(result_os.replace("\n",""))

    print('site_new_ip: ', site_new_ip)

    if site_dict.get(site_url) != None:

        site_old_ip = site_dict[site_url]
        i = 0
        ip_changed = False
        while i < len(site_old_ip):
            if site_old_ip[i] == site_new_ip[i]:
                print(f'{site_url} - {site_old_ip[i]}.')
            else:
                print(f'[ERROR] {site_url} IP mismatch: {site_old_ip[i]} {site_new_ip[i]}.')
                site_dict[site_url] = site_new_ip
                ip_changed = True
            i = i + 1

    else:
        #If it's first execution
        site_dict[site_url] = site_new_ip
        print('site_dict==', site_dict)
        ip_changed = True

    if ip_changed == True:
        with open("servers_ip.json", "w") as fp_json:
            json.dump(site_dict, fp_json, indent=2)
        with open("servers_ip.yaml", "w") as fp_yaml:
            yaml.dump(site_dict, fp_yaml, explicit_start=True, explicit_end=True)

    return site_dict

while True:
    site_dict = check_list_of_sites(site_list, site_dict)
    print("site_dict==", site_dict)
    time.sleep(5)

```

#### Вывод скрипта при запуске при тестировании:
```shell
site_dict== {'drive.google.com': ['74.125.131.194'], 'mail.google.com': ['64.233.161.17'], 'google.com': ['173.194.73.139']}
site_new_ip:  ['74.125.131.194']
drive.google.com - 74.125.131.194.
site_new_ip:  ['64.233.161.83']
[ERROR] mail.google.com IP mismatch: 64.233.161.17 64.233.161.83.
site_new_ip:  ['173.194.73.101']
[ERROR] google.com IP mismatch: 173.194.73.139 173.194.73.101.
site_dict== {'drive.google.com': ['74.125.131.194'], 'mail.google.com': ['64.233.161.83'], 'google.com': ['173.194.73.101']}
site_new_ip:  ['74.125.131.194']
drive.google.com - 74.125.131.194.
site_new_ip:  ['64.233.161.83']
mail.google.com - 64.233.161.83.
site_new_ip:  ['173.194.73.101']
google.com - 173.194.73.101.
```

#### json-файл(ы), который(е) записал ваш скрипт:
```json
{
  "drive.google.com": [
    "74.125.131.194"
  ],
  "mail.google.com": [
    "64.233.161.83"
  ],
  "google.com": [
    "173.194.73.101"
  ]
}
```

#### yml-файл(ы), который(е) записал ваш скрипт:
```yaml
---
drive.google.com:
- 74.125.131.194
google.com:
- 173.194.73.101
mail.google.com:
- 64.233.161.83
...
```

