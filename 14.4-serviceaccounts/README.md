# Домашнее задание к занятию "14.4 Сервис-аккаунты"

## Задача 1: Работа с сервис-аккаунтами через утилиту kubectl в установленном minikube

Выполните приведённые команды в консоли. Получите вывод команд. Сохраните
задачу 1 как справочный материал.

### Как создать сервис-аккаунт?

```
kubectl create serviceaccount netology
```
```commandline
anton@DevOps:~/Desktop/14.4$ sudo kubectl create serviceaccount netology
serviceaccount/netology created
```
### Как просмотреть список сервис-акаунтов?

```
kubectl get serviceaccounts
kubectl get serviceaccount
```
```commandline
anton@DevOps:~/Desktop/14.4$ sudo kubectl get serviceaccounts
NAME       SECRETS   AGE
default    0         104d
netology   0         14s
anton@DevOps:~/Desktop/14.4$ sudo kubectl get serviceaccount
NAME       SECRETS   AGE
default    0         104d
netology   0         23s
```
### Как получить информацию в формате YAML и/или JSON?

```
kubectl get serviceaccount netology -o yaml
kubectl get serviceaccount default -o json
```
```commandline
anton@DevOps:~/Desktop/14.4$ sudo kubectl get serviceaccount netology -o yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  creationTimestamp: "2023-02-05T17:55:34Z"
  name: netology
  namespace: default
  resourceVersion: "7410"
  uid: 667ff7e7-151e-49a2-b91b-f14f1a3b2d39
anton@DevOps:~/Desktop/14.4$ sudo kubectl get serviceaccount default -o json
{
    "apiVersion": "v1",
    "kind": "ServiceAccount",
    "metadata": {
        "creationTimestamp": "2022-10-24T15:58:27Z",
        "name": "default",
        "namespace": "default",
        "resourceVersion": "326",
        "uid": "34bcfb1e-efd0-423b-aca6-c37f82287825"
    }
}
```
### Как выгрузить сервис-акаунты и сохранить его в файл?

```
kubectl get serviceaccounts -o json > serviceaccounts.json
kubectl get serviceaccount netology -o yaml > netology.yml
```
```commandline
anton@DevOps:~/Desktop/14.4$ sudo kubectl get serviceaccounts -o json > serviceaccounts.json
anton@DevOps:~/Desktop/14.4$ sudo kubectl get serviceaccount netology -o yaml > netology.yml
anton@DevOps:~/Desktop/14.4$ ll
total 16
drwxrwxr-x 2 anton anton 4096 фев  5 20:57 ./
drwxr-xr-x 9 anton anton 4096 фев  5 20:52 ../
-rw-rw-r-- 1 anton anton  198 фев  5 20:57 netology.yml
-rw-rw-r-- 1 anton anton  867 фев  5 20:57 serviceaccounts.json
```
### Как удалить сервис-акаунт?

```
kubectl delete serviceaccount netology
```
```commandline
anton@DevOps:~/Desktop/14.4$ sudo kubectl delete serviceaccount netology
serviceaccount "netology" deleted
```
### Как загрузить сервис-акаунт из файла?

```
kubectl apply -f netology.yml
```
```commandline
anton@DevOps:~/Desktop/14.4$ sudo kubectl apply -f netology.yml
serviceaccount/netology created
```

## Задача 2 (*): Работа с сервис-акаунтами внутри модуля

Выбрать любимый образ контейнера, подключить сервис-акаунты и проверить
доступность API Kubernetes

```
kubectl run -i --tty fedora --image=fedora --restart=Never -- sh
```

Просмотреть переменные среды

```
env | grep KUBE
```
```commandline
anton@DevOps:~/Desktop/14.4$ sudo kubectl run -i --tty fedora --image=fedora --restart=Never -- sh
If you don't see a command prompt, try pressing enter.
sh-5.2# env | grep KUBE
KUBERNETES_SERVICE_PORT_HTTPS=443
KUBERNETES_SERVICE_PORT=443
KUBERNETES_PORT_443_TCP=tcp://10.96.0.1:443
KUBERNETES_PORT_443_TCP_PROTO=tcp
KUBERNETES_PORT_443_TCP_ADDR=10.96.0.1
KUBERNETES_SERVICE_HOST=10.96.0.1
KUBERNETES_PORT=tcp://10.96.0.1:443
KUBERNETES_PORT_443_TCP_PORT=443
```
Получить значения переменных

```
K8S=https://$KUBERNETES_SERVICE_HOST:$KUBERNETES_SERVICE_PORT
SADIR=/var/run/secrets/kubernetes.io/serviceaccount
TOKEN=$(cat $SADIR/token)
CACERT=$SADIR/ca.crt
NAMESPACE=$(cat $SADIR/namespace)
```

Подключаемся к API

```
curl -H "Authorization: Bearer $TOKEN" --cacert $CACERT $K8S/api/v1/
```
```commandline
sh-5.2# curl -H "Authorization: Bearer $TOKEN" --cacert $CACERT $K8S/api/v1/
{
  "kind": "APIResourceList",
  "groupVersion": "v1",
  "resources": [
    {
      "name": "bindings",
      "singularName": "",
      "namespaced": true,
      "kind": "Binding",
      "verbs": [
        "create"
      ]
    },
    {
      "name": "componentstatuses",
      "singularName": "",
      "namespaced": false,
      "kind": "ComponentStatus",
      "verbs": [
        "get",
        "list"
      ],
      "shortNames": [
        "cs"
      ]
    },
    
...

{
      "name": "services/proxy",
      "singularName": "",
      "namespaced": true,
      "kind": "ServiceProxyOptions",
      "verbs": [
        "create",
        "delete",
        "get",
        "patch",
        "update"
      ]
    },
    {
      "name": "services/status",
      "singularName": "",
      "namespaced": true,
      "kind": "Service",
      "verbs": [
        "get",
        "patch",
        "update"
      ]
    }
  ]

```

В случае с minikube может быть другой адрес и порт, который можно взять здесь

```
cat ~/.kube/config
```

или здесь

```
kubectl cluster-info
```

---

### Как оформить ДЗ?

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

В качестве решения прикрепите к ДЗ конфиг файлы для деплоя. Прикрепите скриншоты вывода команды kubectl со списком запущенных объектов каждого типа (pods, deployments, serviceaccounts) или скриншот из самого Kubernetes, что сервисы подняты и работают, а также вывод из CLI.

---