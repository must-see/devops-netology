# Домашнее задание к занятию "12.5 Сетевые решения CNI"
После работы с Flannel появилась необходимость обеспечить безопасность для приложения. Для этого лучше всего подойдет Calico.
## Задание 1: установить в кластер CNI плагин Calico
Для проверки других сетевых решений стоит поставить отличный от Flannel плагин — например, Calico. Требования: 
* установка производится через ansible/kubespray;
* после применения следует настроить политику доступа к hello-world извне. Инструкции [kubernetes.io](https://kubernetes.io/docs/concepts/services-networking/network-policies/), [Calico](https://docs.projectcalico.org/about/about-network-policy)


```commandline
anton@node1:~/netpolicy$ sudo kubectl get services
NAME         TYPE           CLUSTER-IP     EXTERNAL-IP      PORT(S)          AGE
hello-node   LoadBalancer   10.233.34.62   192.168.88.195   8080:31248/TCP   17h
kubernetes   ClusterIP      10.233.0.1     <none>           443/TCP          18h
anton@node1:~/netpolicy$ sudo kubectl scale deployment hello-node --replicas=4
deployment.apps/hello-node scaled
anton@node1:~/netpolicy$ sudo kubectl get po -o wide
[sudo] password for anton:
NAME                         READY   STATUS    RESTARTS   AGE    IP              NODE    NOMINATED NODE   READINESS GATES
hello-node-697897c86-j5p4n   1/1     Running   0          19h    10.233.97.130   node5   <none>           <none>
hello-node-697897c86-m47wk   1/1     Running   0          106m   10.233.74.66    node4   <none>           <none>
hello-node-697897c86-s975t   1/1     Running   0          106m   10.233.71.2     node3   <none>           <none>
hello-node-697897c86-ztnp9   1/1     Running   0          106m   10.233.75.2     node2   <none>           <none>

```
```commandline
C:\Users\must->curl -I 192.168.88.195:8080
HTTP/1.1 200 OK
Server: nginx/1.10.0
Date: Sun, 20 Nov 2022 15:29:59 GMT
Content-Type: text/plain
Connection: keep-alive
```
## Задание 2: изучить, что запущено по умолчанию
Самый простой способ — проверить командой calicoctl get <type>. Для проверки стоит получить список нод, ipPool и profile.
Требования: 
* установить утилиту calicoctl;
* получить 3 вышеописанных типа в консоли.

```commandline
anton@node1:~$ sudo calicoctl get node
NAME
node1
node2
node3
node4
node5

anton@node1:~$ sudo calicoctl get ipPool
NAME           CIDR             SELECTOR
default-pool   10.233.64.0/18   all()

anton@node1:~$ sudo calicoctl get profile
NAME
projectcalico-default-allow
kns.default
kns.kube-node-lease
kns.kube-public
kns.kube-system
ksa.default.default
ksa.kube-node-lease.default
ksa.kube-public.default
ksa.kube-system.attachdetach-controller
ksa.kube-system.bootstrap-signer
ksa.kube-system.calico-kube-controllers
ksa.kube-system.calico-node
ksa.kube-system.certificate-controller
ksa.kube-system.clusterrole-aggregation-controller
ksa.kube-system.coredns
ksa.kube-system.cronjob-controller
ksa.kube-system.daemon-set-controller
ksa.kube-system.default
ksa.kube-system.deployment-controller
ksa.kube-system.disruption-controller
ksa.kube-system.dns-autoscaler
ksa.kube-system.endpoint-controller
ksa.kube-system.endpointslice-controller
ksa.kube-system.endpointslicemirroring-controller
ksa.kube-system.ephemeral-volume-controller
ksa.kube-system.expand-controller
ksa.kube-system.generic-garbage-collector
ksa.kube-system.horizontal-pod-autoscaler
ksa.kube-system.job-controller
ksa.kube-system.kube-proxy
ksa.kube-system.namespace-controller
ksa.kube-system.node-controller
ksa.kube-system.nodelocaldns
ksa.kube-system.persistent-volume-binder
ksa.kube-system.pod-garbage-collector
ksa.kube-system.pv-protection-controller
ksa.kube-system.pvc-protection-controller
ksa.kube-system.replicaset-controller
ksa.kube-system.replication-controller
ksa.kube-system.resourcequota-controller
ksa.kube-system.root-ca-cert-publisher
ksa.kube-system.service-account-controller
ksa.kube-system.service-controller
ksa.kube-system.statefulset-controller
ksa.kube-system.token-cleaner
ksa.kube-system.ttl-after-finished-controller
ksa.kube-system.ttl-controller

```
### Как оформить ДЗ?

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.