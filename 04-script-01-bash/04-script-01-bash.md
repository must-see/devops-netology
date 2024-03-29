### Домашнее задание к занятию "4.1. Командная оболочка Bash: Практические навыки"

#### 1. Есть скрипт:
```bash
	a=1
	b=2
	c=a+b
	d=$a+$b
	e=$(($a+$b))
```
	* Какие значения переменным c,d,e будут присвоены?
	* Почему?
- `c=a+b` вернет `a+b`, т.к. `a` и `b` без символа `$`.
```shell
echo $c
a+b
```
- `d=$a+$b` вернет `1+2`, т.к. `a` и `b` с символом `$` будут восприниматься как обращения к переменным
```shell
echo $d
1+2
```
- `e=$(($a+$b))` вернет `3`, т.к. конструкция `((..))` служит для арифметических операций
```shell
echo $e
3
```

#### 2. На нашем локальном сервере упал сервис и мы написали скрипт, который постоянно проверяет его доступность, записывая дату проверок до тех пор, пока сервис не станет доступным. В скрипте допущена ошибка, из-за которой выполнение не может завершиться, при этом место на Жёстком Диске постоянно уменьшается. Что необходимо сделать, чтобы его исправить:
```bash
	while ((1==1)
	do
	curl https://localhost:4757
	if (($? != 0))
	then
	date >> curl.log
	fi
	done
```
```bash
	while ((1==1))              #отсутствовала вторая закрывающаяся круглая скобка
	do
	  curl https://localhost:4757
	if (($? != 0))
	then
	  date >> curl.log
	else                        #<< условие выхода при поднятии сервиса
	  break                     #<< break   
	fi
	done
```
#### 3. Необходимо написать скрипт, который проверяет доступность трёх IP: 192.168.0.1, 173.194.222.113, 87.250.250.242 по 80 порту и записывает результат в файл log. Проверять доступность необходимо пять раз для каждого узла.
```bash
#!/usr/bin/env bash
declare -i i=1
while (($i<=5))
do
  for hosts in 192.168.88.1 87.250.250.242 8.8.8.8; do
    nc -zw1 $hosts 80
    echo $? $hosts `date` >> curl.log
  done
i+=1
sleep 1
done
```
#### 4. Необходимо дописать скрипт из предыдущего задания так, чтобы он выполнялся до тех пор, пока один из узлов не окажется недоступным. Если любой из узлов недоступен - IP этого узла пишется в файл error, скрипт прерывается
```bash
#!/usr/bin/env bash
declare -i i=1
while (($i==1))
do
  for hosts in 192.168.88.1 87.250.250.242 8.8.8.8; do
    nc -zw1 $hosts 80
    if (($?!=0))
    then
      echo $? $hosts `date` >> error.log
      exit 0
    else
      echo $? $hosts `date` >> curl.log
    fi
  done
sleep 1
done
```

 ```bash
cat curl.log
1 192.168.88.1 Sun 13 Mar 2022 04:27:53 PM UTC
1 87.250.250.242 Sun 13 Mar 2022 04:27:53 PM UTC
```

```bash
cat error.log
0 8.8.8.8 Sun 13 Mar 2022 04:27:54 PM UTC
```