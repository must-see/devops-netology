### Домашнее задание к занятию "4.2. Использование Python для решения типовых DevOps задач"

#### Обязательные задания

#### 1. Есть скрипт:
	```python
    #!/usr/bin/env python3
	a = 1
	b = '2'
	c = a + b
	```
	* Какое значение будет присвоено переменной c?
	* Как получить для переменной c значение 12?
	* Как получить для переменной c значение 3?
* Какое значение будет присвоено переменной c? - Интерпретатор выдаст ошибку(unsupported operand type(s) for +: 'int' and 'str) - попытка сложения целочисленного значения со строковым. 
* Как получить для переменной c значение 12?
```python
#!/usr/bin/env python3
a = 1
b = '2'
c = str(a) + b 
```
* Как получить для переменной c значение 3?
```python
#!/usr/bin/env python3
a = 1
b = '2'
c = a + int(b)
```

#### 2. Мы устроились на работу в компанию, где раньше уже был DevOps Engineer. Он написал скрипт, позволяющий узнать, какие файлы модифицированы в репозитории, относительно локальных изменений. Этим скриптом недовольно начальство, потому что в его выводе есть не все изменённые файлы, а также непонятен полный путь к директории, где они находятся. Как можно доработать скрипт ниже, чтобы он исполнял требования вашего руководителя?

	```python
    #!/usr/bin/env python3

    import os

	bash_command = ["cd ~/netology/sysadm-homeworks", "git status"]
	result_os = os.popen(' && '.join(bash_command)).read()
    is_change = False
	for result in result_os.split('\n'):
        if result.find('modified') != -1:
            prepare_result = result.replace('\tmodified:   ', '')
            print(prepare_result)
            break

	```

```python
#!/usr/bin/env python3

import os

basedir = "C:/Users/must-/PycharmProjects/devops-netology"
bash_command = [f"cd {basedir}", "git status "]
result_os = os.popen(' && '.join(bash_command)).read()
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('modified:', basedir)
        print(prepare_result)

```
```shell
 python 2.py
        C:/Users/must-/PycharmProjects/devops-netology   04-script-02-py/04-script-02-py.md
        C:/Users/must-/PycharmProjects/devops-netology   04-script-02-py/2.py
        C:/Users/must-/PycharmProjects/devops-netology   04-script-02-py/3.py
        C:/Users/must-/PycharmProjects/devops-netology   04-script-02-py/4.py

```

#### 3. Доработать скрипт выше так, чтобы он мог проверять не только локальный репозиторий в текущей директории, а также умел воспринимать путь к репозиторию, который мы передаём как входной параметр. Мы точно знаем, что начальство коварное и будет проверять работу этого скрипта в директориях, которые не являются локальными репозиториями.

```python
#!/usr/bin/env python3

import os
import sys

basedir = ""
try:
    basedir = sys.argv[1]
except:
    print("Incorrect repository path")

if basedir != "":
        bash_command = [f"cd {basedir}",  "git status "]
        result_os1 = os.listdir(basedir);

        if result_os1.__contains__(".git"):
                result_os = os.popen(' && '.join(bash_command)).read()
                for result in result_os.split('\n'):
                    if result.find('modified') != -1:
                        prepare_result = result.replace('modified:', basedir)
                        print(prepare_result)
        else:
                print("There is no git repository on the entered path")

```
```shell
python 3.py
Incorrect repository path

python 3.py C:/Users/must-/PycharmProjects/devops-netology
        C:/Users/must-/PycharmProjects/devops-netology   04-script-02-py/04-script-02-py.md
        C:/Users/must-/PycharmProjects/devops-netology   04-script-02-py/2.py
        C:/Users/must-/PycharmProjects/devops-netology   04-script-02-py/3.py
        C:/Users/must-/PycharmProjects/devops-netology   04-script-02-py/4.py

python 3.py C:/Users/must-/PycharmProjects/               
There is no git repository on the entered path

```


#### 4. Наша команда разрабатывает несколько веб-сервисов, доступных по http. Мы точно знаем, что на их стенде нет никакой балансировки, кластеризации, за DNS прячется конкретный IP сервера, где установлен сервис. Проблема в том, что отдел, занимающийся нашей инфраструктурой очень часто меняет нам сервера, поэтому IP меняются примерно раз в неделю, при этом сервисы сохраняют за собой DNS имена. Это бы совсем никого не беспокоило, если бы несколько раз сервера не уезжали в такой сегмент сети нашей компании, который недоступен для разработчиков. Мы хотим написать скрипт, который опрашивает веб-сервисы, получает их IP, выводит информацию в стандартный вывод в виде: <URL сервиса> - <его IP>. Также, должна быть реализована возможность проверки текущего IP сервиса c его IP из предыдущей проверки. Если проверка будет провалена - оповестить об этом в стандартный вывод сообщением: [ERROR] <URL сервиса> IP mismatch: <старый IP> <Новый IP>. Будем считать, что наша разработка реализовала сервисы: drive.google.com, mail.google.com, google.com.

```python
#!/usr/bin/env python3

import socket
from string import whitespace

hosts = ["drive.google.com", "mail.google.com", "google.com"]
fileList = []

with open('host.log') as file:
    for f in file:
        fileList.append(f)

with open('host.log', 'w+') as file:
    for i in hosts:
        result = socket.gethostbyname(i)
        added = 0
        for y in fileList:
            inList = y.find(" {}".format(i))
            if (inList != -1):
                ipstr=y.replace('\n', '').split("  ")[1].translate({None: whitespace})
                if (ipstr == result):
                    print(" {}  {}\n".format(i, result))
                    file.write(" {}  {}\n".format(i, result))
                    added = 1
                    break
                else:
                    print("[ERROR] {} IP mismatch: {}  {}\n".format(i, ipstr, result))
                    file.write("[ERROR] {} IP mismatch: {}  {}\n".format(i, ipstr, result))
                    added = 1
                    break
        if (added == 0):
            print(" {}  {}\n".format(i, result))
            file.write(" {}  {}\n".format(i, result))

```
```shell
 python 4.py
 drive.google.com  173.194.73.100

 mail.google.com  64.233.161.17

 google.com  142.250.74.46
```
ipconfig /flushdns - очистка DNS кэша
```shell
python 4.py
[ERROR] drive.google.com IP mismatch: 173.194.73.100  173.194.73.113

[ERROR] mail.google.com IP mismatch: 64.233.161.17  64.233.161.19

 google.com  142.250.74.46

```