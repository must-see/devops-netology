# Домашнее задание к занятию "12.4 Развертывание кластера на собственных серверах, лекция 2"
Новые проекты пошли стабильным потоком. Каждый проект требует себе несколько кластеров: под тесты и продуктив. Делать все руками — не вариант, поэтому стоит автоматизировать подготовку новых кластеров.

## Задание 1: Подготовить инвентарь kubespray
Новые тестовые кластеры требуют типичных простых настроек. Нужно подготовить инвентарь и проверить его работу. Требования к инвентарю:
* подготовка работы кластера из 5 нод: 1 мастер и 4 рабочие ноды;
* в качестве CRI — containerd;
* запуск etcd производить на мастере.

[Установка Kubernetes с помощью kubespray](https://github.com/aak74/kubernetes-for-beginners/tree/master/15-install/30-kubespray)

- hosts.yaml
```yaml
all:
  hosts:
    node1:
      ansible_host: 192.168.88.190
      ip: 192.168.88.190
      access_ip: 192.168.88.190
      ansible_ssh_user: anton
      ansible_ssh_pass: P@ssword
    node2:
      ansible_host: 192.168.88.191
      ip: 192.168.88.191
      access_ip: 192.168.88.191
      ansible_ssh_user: anton
      ansible_ssh_pass: P@ssword
    node3:
      ansible_host: 192.168.88.192
      ip: 192.168.88.192
      access_ip: 192.168.88.192
      ansible_ssh_user: anton
      ansible_ssh_pass: P@ssword
    node4:
      ansible_host: 192.168.88.193
      ip: 192.168.88.193
      access_ip: 192.168.88.193
      ansible_ssh_user: anton
      ansible_ssh_pass: P@ssword
    node5:
      ansible_host: 192.168.88.194
      ip: 192.168.88.194
      access_ip: 192.168.88.194
      ansible_ssh_user: anton
      ansible_ssh_pass: P@ssword
  children:
    kube_control_plane:
      hosts:
        node1:
    kube_node:
      hosts:
        node2:
        node3:
        node4:
        node5:
    etcd:
      hosts:
        node1:
    k8s_cluster:
      children:
        kube_control_plane:
        kube_node:
    calico_rr:
      hosts: {}
```

sudo apt-get install sshpass

```commandline
ansible-playbook -i inventory/mycluster/hosts.yaml cluster.yml -b -v -kK

PLAY RECAP *********************************************************************************************************************************************************
localhost                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
node1                      : ok=746  changed=157  unreachable=0    failed=0    skipped=1239 rescued=0    ignored=9   
node2                      : ok=523  changed=103  unreachable=0    failed=0    skipped=758  rescued=0    ignored=2   
node3                      : ok=523  changed=103  unreachable=0    failed=0    skipped=757  rescued=0    ignored=2   
node4                      : ok=523  changed=103  unreachable=0    failed=0    skipped=757  rescued=0    ignored=2   
node5                      : ok=523  changed=103  unreachable=0    failed=0    skipped=757  rescued=0    ignored=2   

Суббота 19 ноября 2022  22:19:22 +0300 (0:00:00.218)       0:17:59.630 ******** 
=============================================================================== 
download : download_container | Download image if required ------------------------------------------------------------------------------------------------- 54.71s
download : download_file | Download item ------------------------------------------------------------------------------------------------------------------- 51.34s
download : download_container | Download image if required ------------------------------------------------------------------------------------------------- 42.21s
kubernetes/preinstall : Install packages requirements ------------------------------------------------------------------------------------------------------ 39.88s
kubernetes/kubeadm : Join to cluster ----------------------------------------------------------------------------------------------------------------------- 38.75s
download : download_container | Download image if required ------------------------------------------------------------------------------------------------- 30.40s
download : download_file | Download item ------------------------------------------------------------------------------------------------------------------- 26.52s
download : download_file | Validate mirrors ---------------------------------------------------------------------------------------------------------------- 24.42s
download : download_container | Download image if required ------------------------------------------------------------------------------------------------- 22.28s
container-engine/containerd : download_file | Download item ------------------------------------------------------------------------------------------------ 21.02s
download : download_container | Download image if required ------------------------------------------------------------------------------------------------- 20.44s
download : download_container | Download image if required ------------------------------------------------------------------------------------------------- 18.33s
download : download_file | Download item ------------------------------------------------------------------------------------------------------------------- 16.70s
download : download_file | Download item ------------------------------------------------------------------------------------------------------------------- 16.60s
download : download_container | Download image if required ------------------------------------------------------------------------------------------------- 16.23s
kubernetes/control-plane : kubeadm | Initialize first master ----------------------------------------------------------------------------------------------- 14.35s
container-engine/crictl : download_file | Download item ---------------------------------------------------------------------------------------------------- 11.41s
download : download_container | Download image if required ------------------------------------------------------------------------------------------------- 11.08s
download : download_container | Download image if required ------------------------------------------------------------------------------------------------- 10.73s
etcd : reload etcd ------------------------------------------------------------------------------------------------------------------------------------------ 8.87s
```
```commandline
anton@node1:~$ kubectl version
WARNING: This version information is deprecated and will be replaced with the ou                                                                                                                                                             tput from kubectl version --short.  Use --output=yaml|json to get the full versi                                                                                                                                                             on.
Client Version: version.Info{Major:"1", Minor:"25", GitVersion:"v1.25.4", GitCom                                                                                                                                                             mit:"872a965c6c6526caa949f0c6ac028ef7aff3fb78", GitTreeState:"clean", BuildDate:                                                                                                                                                             "2022-11-09T13:36:36Z", GoVersion:"go1.19.3", Compiler:"gc", Platform:"linux/amd                                                                                                                                                             64"}
Kustomize Version: v4.5.7

anton@node1:~$ sudo kubectl get nodes
[sudo] password for anton:
NAME    STATUS   ROLES           AGE     VERSION
node1   Ready    control-plane   5m31s   v1.25.4
node2   Ready    <none>          4m23s   v1.25.4
node3   Ready    <none>          4m23s   v1.25.4
node4   Ready    <none>          4m23s   v1.25.4
node5   Ready    <none>          4m23s   v1.25.4

anton@node1:~$ sudo kubectl create deploy nginx --image=nginx:latest --replicas=2
deployment.apps/nginx created

anton@node1:~$ sudo kubectl get po -o wide
NAME                     READY   STATUS    RESTARTS   AGE   IP              NODE    NOMINATED NODE   READINESS GATES
nginx-6d666844f6-b9kwd   1/1     Running   0          65s   10.233.75.1     node2   <none>           <none>
nginx-6d666844f6-z25hr   1/1     Running   0          65s   10.233.97.129   node5   <none>           <none>

```

## Задание 2 (*): подготовить и проверить инвентарь для кластера в AWS
Часть новых проектов хотят запускать на мощностях AWS. Требования похожи:
* разворачивать 5 нод: 1 мастер и 4 рабочие ноды;
* работать должны на минимально допустимых EC2 — t3.small.

---

### Как оформить ДЗ?

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---