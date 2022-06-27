# Домашнее задание к занятию "7.1. Инфраструктура как код"

## Задача 1. Выбор инструментов. 
 
### Легенда
 
Через час совещание на котором менеджер расскажет о новом проекте. Начать работу над которым надо 
будет уже сегодня. 
На данный момент известно, что это будет сервис, который ваша компания будет предоставлять внешним заказчикам.
Первое время, скорее всего, будет один внешний клиент, со временем внешних клиентов станет больше.

Так же по разговорам в компании есть вероятность, что техническое задание еще не четкое, что приведет к большому
количеству небольших релизов, тестирований интеграций, откатов, доработок, то есть скучно не будет.  
   
Вам, как девопс инженеру, будет необходимо принять решение об инструментах для организации инфраструктуры.
На данный момент в вашей компании уже используются следующие инструменты: 
- остатки Сloud Formation, 
- некоторые образы сделаны при помощи Packer,
- год назад начали активно использовать Terraform, 
- разработчики привыкли использовать Docker, 
- уже есть большая база Kubernetes конфигураций, 
- для автоматизации процессов используется Teamcity, 
- также есть совсем немного Ansible скриптов, 
- и ряд bash скриптов для упрощения рутинных задач.  

Для этого в рамках совещания надо будет выяснить подробности о проекте, что бы в итоге определиться с инструментами:

1. Какой тип инфраструктуры будем использовать для этого проекта: изменяемый или не изменяемый?
```commandline
Неизменяемый
```
2. Будет ли центральный сервер для управления инфраструктурой?
```commandline
Нет, управление будет с любой машины через Terraform/Ansible
```
3. Будут ли агенты на серверах?
```commandline
Нет, используем безагентный подход
```
4. Будут ли использованы средства для управления конфигурацией или инициализации ресурсов? 
```commandline
Да, Terraform\Ansible
```
В связи с тем, что проект стартует уже сегодня, в рамках совещания надо будет определиться со всеми этими вопросами.

### В результате задачи необходимо

1. Ответить на четыре вопроса представленных в разделе "Легенда". 
2. Какие инструменты из уже используемых вы хотели бы использовать для нового проекта? 
```commandline
Packer, Terraform, Docker, Kubernetes, Ansible, Teamcity
```
3. Хотите ли рассмотреть возможность внедрения новых инструментов для этого проекта? 
```commandline
Нет
```

Если для ответа на эти вопросы недостаточно информации, то напишите какие моменты уточните на совещании.


## Задача 2. Установка терраформ. 

Официальный сайт: https://www.terraform.io/

Установите терраформ при помощи менеджера пакетов используемого в вашей операционной системе.
В виде результата этой задачи приложите вывод команды `terraform --version`.
```commandline
anton@ubuntu:~$ terraform --version
Terraform v1.0.8
on linux_amd64
```

## Задача 3. Поддержка легаси кода. 

В какой-то момент вы обновили терраформ до новой версии, например с 0.12 до 0.13. 
А код одного из проектов настолько устарел, что не может работать с версией 0.13. 
В связи с этим необходимо сделать так, чтобы вы могли одновременно использовать последнюю версию терраформа установленную при помощи
штатного менеджера пакетов и устаревшую версию 0.12. 

В виде результата этой задачи приложите вывод `--version` двух версий терраформа доступных на вашем компьютере 
или виртуальной машине.
```commandline
anton@ubuntu:~$ git clone https://github.com/tfutils/tfenv.git ~/.tfenv
Cloning into '/home/anton/.tfenv'...
remote: Enumerating objects: 1569, done.
remote: Counting objects: 100% (384/384), done.
remote: Compressing objects: 100% (157/157), done.
remote: Total 1569 (delta 240), reused 336 (delta 213), pack-reused 1185
Receiving objects: 100% (1569/1569), 337.37 KiB | 2.02 MiB/s, done.
Resolving deltas: 100% (1003/1003), done.
anton@ubuntu:~$ echo 'export PATH="$HOME/.tfenv/bin:$PATH"' >> ~/.bash_profile
anton@ubuntu:~$ mkdir -p ~/.local/bin/
anton@ubuntu:~$ . ~/.profile
anton@ubuntu:~$ ln -s ~/.tfenv/bin/* ~/.local/bin
anton@ubuntu:~$ which tfenv
/home/anton/.local/bin/tfenv
anton@ubuntu:~$ tfenv list
No versions available. Please install one with: tfenv install
anton@ubuntu:~$ tfenv list-remote
1.3.0-alpha20220622
1.3.0-alpha20220608
1.2.3
1.2.2
1.2.1
1.2.0
...
anton@ubuntu:~$ tfenv install 1.0.8
Installing Terraform v1.0.8
Downloading release tarball from https://releases.hashicorp.com/terraform/1.0.8/terraform_1.0.8_linux_amd64.zip
#################################################################################################################################################################################################### 100.0%
Downloading SHA hash file from https://releases.hashicorp.com/terraform/1.0.8/terraform_1.0.8_SHA256SUMS
No keybase install found, skipping OpenPGP signature verification
Archive:  /tmp/tfenv_download.CCw2J6/terraform_1.0.8_linux_amd64.zip
  inflating: /home/anton/.tfenv/versions/1.0.8/terraform  
Installation of terraform v1.0.8 successful. To make this your default version, run 'tfenv use 1.0.8'
anton@ubuntu:~$ tfenv install latest
Installing Terraform v1.2.3
Downloading release tarball from https://releases.hashicorp.com/terraform/1.2.3/terraform_1.2.3_linux_amd64.zip
#################################################################################################################################################################################################### 100.0%
Downloading SHA hash file from https://releases.hashicorp.com/terraform/1.2.3/terraform_1.2.3_SHA256SUMS
No keybase install found, skipping OpenPGP signature verification
Archive:  /tmp/tfenv_download.aZgKwM/terraform_1.2.3_linux_amd64.zip
  inflating: /home/anton/.tfenv/versions/1.2.3/terraform  
Installation of terraform v1.2.3 successful. To make this your default version, run 'tfenv use 1.2.3'
anton@ubuntu:~$ tfenv list
  1.2.3
  1.0.8
No default set. Set with 'tfenv use <version>'
anton@ubuntu:~$ tfenv use
cat: /home/anton/.tfenv/version: No such file or directory
Switching default version to v1.2.3
Switching completed
anton@ubuntu:~$ terraform --version
Terraform v1.2.3
on linux_amd64
anton@ubuntu:~$ tfenv use
Switching default version to v1.2.3
Switching completed
anton@ubuntu:~$ tfenv use 1.0.8
Switching default version to v1.0.8
Switching completed
anton@ubuntu:~$ terraform --version
Terraform v1.0.8
on linux_amd64
```

```commandline
https://github.com/tfutils/tfenv#installation
https://opensource.com/article/20/11/tfenv
```

---

### Как cдавать задание

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---