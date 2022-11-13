# Домашнее задание к занятию "12.2 Команды для работы с Kubernetes"
Кластер — это сложная система, с которой крайне редко работает один человек. Квалифицированный devops умеет наладить работу всей команды, занимающейся каким-либо сервисом.
После знакомства с кластером вас попросили выдать доступ нескольким разработчикам. Помимо этого требуется служебный аккаунт для просмотра логов.

## Задание 1: Запуск пода из образа в деплойменте
Для начала следует разобраться с прямым запуском приложений из консоли. Такой подход поможет быстро развернуть инструменты отладки в кластере. Требуется запустить деплоймент на основе образа из hello world уже через deployment. Сразу стоит запустить 2 копии приложения (replicas=2). 

Требования:
 * пример из hello world запущен в качестве deployment
 * количество реплик в deployment установлено в 2
 * наличие deployment можно проверить командой kubectl get deployment
 * наличие подов можно проверить командой kubectl get pods

```commandline
anton@ubuntu:~/Desktop/HW$ sudo kubectl create deployment hello-deployment --image=k8s.gcr.io/echoserver:1.4 --replicas=2
deployment.apps/hello-deployment created
anton@ubuntu:~/Desktop/HW$ sudo kubectl get deployments
NAME               READY   UP-TO-DATE   AVAILABLE   AGE
hello-deployment   2/2     2            2           8s
nton@ubuntu:~/Desktop/HW$ sudo kubectl get pods
NAME                                READY   STATUS    RESTARTS   AGE
hello-deployment-6d464b5885-fmfct   1/1     Running   0          53s
hello-deployment-6d464b5885-jpfcc   1/1     Running   0          53s
```

## Задание 2: Просмотр логов для разработки
Разработчикам крайне важно получать обратную связь от штатно работающего приложения и, еще важнее, об ошибках в его работе. 
Требуется создать пользователя и выдать ему доступ на чтение конфигурации и логов подов в app-namespace.

Требования: 
 * создан новый токен доступа для пользователя
 * пользователь прописан в локальный конфиг (~/.kube/config, блок users)
 * пользователь может просматривать логи подов и их конфигурацию (kubectl logs pod <pod_id>, kubectl describe pod <pod_id>)

Создание пользователя developer, потом создание сертификатов и подпись сертификатами кубернетиса
```commandline
anton@ubuntu:~/Desktop/HW$ sudo useradd developer
anton@ubuntu:~/Desktop/HW$ sudo mkhomedir_helper developer
anton@ubuntu:~/Desktop/HW$ cd /home/developer
anton@ubuntu:/home/developer$ sudo openssl genrsa -out developer.key 2048
Generating RSA private key, 2048 bit long modulus (2 primes)
....................................................................................................................+++++
...........+++++
e is 65537 (0x010001)
anton@ubuntu:/home/developer$ sudo openssl req -new -key developer.key -out developer.csr -subj "/CN=developer"
anton@ubuntu:/home/developer$ sudo openssl x509 -req -in developer.csr -CA /home/p/.minikube/ca.crt -CAkey /home/p/.minikube/ca.key -CAcreateserial -out developer.crt -days 500
Signature ok
subject=CN = developer

anton@ubuntu:/home/developer$ sudo openssl x509 -req -in developer.csr -CA /root/.minikube/ca.crt -CAkey /root/.minikube/ca.key -CAcreateserial -out developer.crt -days 500
Signature ok
subject=CN = developer
Getting CA Private Key

anton@ubuntu:/home/developer$ sudo mkdir .certs
anton@ubuntu:/home/developer$ sudo mv developer.crt developer.key .certs
anton@ubuntu:/home/developer$ sudo chown -R anton: /home/developer/.certs


anton@ubuntu:/home/developer$ kubectl config view | grep -A8 users
users:
- name: developer
  user:
    client-certificate: /home/developer/.certs/developer.crt
    client-key: /home/developer/.certs/developer.key
```
Создаем новый контекст для работы из под developer
```commandline
anton@ubuntu:/home/developer$ sudo kubectl config set-context developer --cluster=minikube --user=developer
Context "developer" created.
anton@ubuntu:/home/developer$ sudo kubectl config use-context developer
Switched to context "developer".
anton@ubuntu:/home/developer$ sudo kubectl config get-contexts
CURRENT   NAME        CLUSTER    AUTHINFO    NAMESPACE
*         developer   minikube   developer   
          minikube    minikube   minikube    default
```
Создаем role.yml и rolebinding.yml
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: role.yml
  namespace: default
rules:
- apiGroups: [ "" ]
  resources: [ pods, pods/log ]
  verbs: [ get, list ]
```
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: developer
  namespace: default
subjects:
- kind: User
  name: developer
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: role.yml
  apiGroup: rbac.authorization.k8s.io
```

```commandline
anton@ubuntu:/home/developer$ sudo kubectl create -f role.yml 
clusterrole.rbac.authorization.k8s.io/role.yml created


anton@ubuntu:/home/developer$ sudo kubectl apply -f rolebinding.yml 
rolebinding.rbac.authorization.k8s.io/developer created

anton@ubuntu:/home/developer$ sudo kubectl config use-context developer
Switched to context "developer".
anton@ubuntu:/home/developer$ sudo kubectl get pods 
NAME                                READY   STATUS    RESTARTS   AGE
hello-deployment-6d464b5885-bhdb4   1/1     Running   0          61m
hello-deployment-6d464b5885-w9cvx   1/1     Running   0          61m

anton@ubuntu:/home/developer$ sudo kubectl logs hello-deployment-6d464b5885-bhdb4
```
Проверка, что внесение изменений запрещено
```commandline
anton@ubuntu:/home/developer$ sudo kubectl apply -f rolebinding.yml 
Error from server (Forbidden): error when retrieving current configuration of:
Resource: "rbac.authorization.k8s.io/v1, Resource=rolebindings", GroupVersionKind: "rbac.authorization.k8s.io/v1, Kind=RoleBinding"
Name: "developer", Namespace: "default"
from server for: "rolebinding.yml": rolebindings.rbac.authorization.k8s.io "developer" is forbidden: User "developer" cannot get resource "rolebindings" in API group "rbac.authorization.k8s.io" in the namespace "default"

```
## Задание 3: Изменение количества реплик 
Поработав с приложением, вы получили запрос на увеличение количества реплик приложения для нагрузки. Необходимо изменить запущенный deployment, увеличив количество реплик до 5. Посмотрите статус запущенных подов после увеличения реплик. 

Требования:
 * в deployment из задания 1 изменено количество реплик на 5
 * проверить что все поды перешли в статус running (kubectl get pods)

---

```commandline
anton@ubuntu:~/Desktop/HW$ sudo kubectl scale --replicas=5 deployment hello-deployment
deployment.apps/hello-deployment scaled
anton@ubuntu:~/Desktop/HW$ sudo kubectl get pods
NAME                                READY   STATUS    RESTARTS   AGE
hello-deployment-6d464b5885-cdzb2   1/1     Running   0          5s
hello-deployment-6d464b5885-cfmpx   1/1     Running   0          5s
hello-deployment-6d464b5885-csqd2   1/1     Running   0          5s
hello-deployment-6d464b5885-fmfct   1/1     Running   0          3m24s
hello-deployment-6d464b5885-jpfcc   1/1     Running   0          3m24s

```

### Как оформить ДЗ?

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---