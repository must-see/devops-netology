## Домашнее задание к занятию "5.2. Применение принципов IaaC в работе с виртуальными машинами" 

###Задача 1
Опишите своими словами основные преимущества применения на практике IaaC паттернов.
```
Основными преимеществами IaaC паттернов являются: 
Быстрое разворачивание инфраструктуры, ускорение разработки и внедрения,
Исключаение "дрейфа" конфигураций.
```

Какой из принципов IaaC является основополагающим?
```
Идемпотентность - свойство при повторении, получать идентичную конфигурацию
```

###Задача 2
Чем Ansible выгодно отличается от других систем управление конфигурациями?
```
Работа через SSH, не требуется установка агентов
```
Какой, на ваш взгляд, метод работы систем конфигурации более надёжный push или pull?
```
pull лучше, т.к. хост может быть выключен и когда включится, тогда и запросит обновление конфигурации.
```

###Задача 3
УУстановить на личный компьютер:

VirtualBox
Vagrant
Ansible

```bash
VBoxManage --version
6.1.32r149290

vagrant --version
Vagrant 2.2.19

ansible --version
ansible 2.9.6
  config file = /etc/ansible/ansible.cfg
  configured module search path = ['/home/vagrant/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python3/dist-packages/ansible
  executable location = /usr/bin/ansible
  python version = 3.8.10 (default, Nov 26 2021, 20:14:08) [GCC 9.3.0]
```

###Задача 4 (*)
Воспроизвести практическую часть лекции самостоятельно. 

```bash
vagrant@server1:~$ sudo docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```