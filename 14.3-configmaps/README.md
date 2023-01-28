# Домашнее задание к занятию "14.3 Карты конфигураций"

## Задача 1: Работа с картами конфигураций через утилиту kubectl в установленном minikube

Выполните приведённые команды в консоли. Получите вывод команд. Сохраните
задачу 1 как справочный материал.

### Как создать карту конфигураций?

```
kubectl create configmap nginx-config --from-file=nginx.conf
kubectl create configmap domain --from-literal=name=netology.ru
```
```commandline
anton@DevOps:~$ sudo kubectl create configmap nginx-config --from-file=nginx.conf
configmap/nginx-config created
anton@DevOps:~$ sudo kubectl create configmap domain --from-literal=name=netology.ru
configmap/domain created
```
### Как просмотреть список карт конфигураций?

```
kubectl get configmaps
kubectl get configmap
```
```commandline
anton@DevOps:~$ sudo kubectl get configmaps
NAME               DATA   AGE
domain             1      30s
kube-root-ca.crt   1      96d
nginx-config       1      56s
anton@DevOps:~$ sudo kubectl get configmap
NAME               DATA   AGE
domain             1      42s
kube-root-ca.crt   1      96d
nginx-config       1      68s
```
### Как просмотреть карту конфигурации?

```
kubectl get configmap nginx-config
kubectl describe configmap domain
```
```commandline
anton@DevOps:~$ sudo kubectl get configmap nginx-config
NAME           DATA   AGE
nginx-config   1      5m52s
anton@DevOps:~$ sudo kubectl describe configmap domain
Name:         domain
Namespace:    default
Labels:       <none>
Annotations:  <none>

Data
====
name:
----
netology.ru

BinaryData
====

Events:  <none>
```
### Как получить информацию в формате YAML и/или JSON?

```
kubectl get configmap nginx-config -o yaml
kubectl get configmap domain -o json
```
```commandline
anton@DevOps:~$ sudo kubectl get configmap nginx-config -o yaml
apiVersion: v1
data:
  nginx.conf: ""
kind: ConfigMap
metadata:
  creationTimestamp: "2023-01-28T18:25:41Z"
  name: nginx-config
  namespace: default
  resourceVersion: "5718"
  uid: 51749f14-bc9d-4137-90b9-55b9394e08b8
anton@DevOps:~$ sudo kubectl get configmap domain -o json
{
    "apiVersion": "v1",
    "data": {
        "name": "netology.ru"
    },
    "kind": "ConfigMap",
    "metadata": {
        "creationTimestamp": "2023-01-28T18:26:07Z",
        "name": "domain",
        "namespace": "default",
        "resourceVersion": "5737",
        "uid": "78c577a9-4d69-4e43-bd47-4057475df8df"
    }
}
```
### Как выгрузить карту конфигурации и сохранить его в файл?

```
kubectl get configmaps -o json > configmaps.json
kubectl get configmap nginx-config -o yaml > nginx-config.yml
```
```commandline
anton@DevOps:~/Desktop/14.3$ sudo kubectl get configmaps -o json > configmaps.json
anton@DevOps:~/Desktop/14.3$ sudo kubectl get configmap nginx-config -o yaml > nginx-config.yml
anton@DevOps:~/Desktop/14.3$ ll
total 16
drwxrwxr-x 2 anton anton 4096 янв 28 21:40 ./
drwxr-xr-x 7 anton anton 4096 янв 28 21:34 ../
-rw-rw-r-- 1 anton anton 2910 янв 28 21:40 configmaps.json
-rw-rw-r-- 1 anton anton  220 янв 28 21:40 nginx-config.yml
```
### Как удалить карту конфигурации?

```
kubectl delete configmap nginx-config
```
```commandline
anton@DevOps:~/Desktop/14.3$ sudo kubectl delete configmap nginx-config
configmap "nginx-config" deleted
```
### Как загрузить карту конфигурации из файла?

```
kubectl apply -f nginx-config.yml
```
```commandline
anton@DevOps:~/Desktop/14.3$ sudo kubectl apply -f nginx-config.yml
configmap/nginx-config created
```
## Задача 2 (*): Работа с картами конфигураций внутри модуля

Выбрать любимый образ контейнера, подключить карты конфигураций и проверить
их доступность как в виде переменных окружения, так и в виде примонтированного
тома

---

### Как оформить ДЗ?

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

В качестве решения прикрепите к ДЗ конфиг файлы для деплоя. Прикрепите скриншоты вывода команды kubectl со списком запущенных объектов каждого типа (pods, deployments, configmaps) или скриншот из самого Kubernetes, что сервисы подняты и работают, а также вывод из CLI.

---