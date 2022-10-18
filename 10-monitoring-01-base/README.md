# Домашнее задание к занятию "10.01. Зачем и что нужно мониторить"

## Обязательные задания

1. Вас пригласили настроить мониторинг на проект. На онбординге вам рассказали, что проект представляет из себя 
платформу для вычислений с выдачей текстовых отчетов, которые сохраняются на диск. Взаимодействие с платформой 
осуществляется по протоколу http. Также вам отметили, что вычисления загружают ЦПУ. Какой минимальный набор метрик вы
выведите в мониторинг и почему?

- __мониторинг операционной системы__:
  - процессор:
    - load average - мониторинг загрузки ЦПУ
  - память:
    - usage - мониторинг использования ОЗУ
    - swap - мониторинг swap
  - диск:
    - Свободное место на диске(ах) с данными
    - скорость записи/чтения
    - latency - мониторинг задержек записи и чтения с дисков
  - сеть:
    - загруженность сетевых интерфейсов
    - drop packet - мониторинг отброшенных пакетов
    

- __мониторинг задействованных сервисов (субд, веб-серверов, файловые хранилища)__:
  - доступность
  - загруженность
  - наличие ошибок
  - время отклика


- __мониторинг приложения__:
  - HTTP-запросы:
    - общее количество запросов
    - количество ошибочных запросов
    - время выполнения запросов
  - операции расчета и вывода данных:
    - количество операций
    - статус операций
    - время исполнения операций
  - Безопасность
    - сколько дней осталось до окончания сертификатов
    - сколько неудачных попыток входа

3. Менеджер продукта посмотрев на ваши метрики сказал, что ему непонятно что такое RAM/inodes/CPUla. Также он сказал, 
что хочет понимать, насколько мы выполняем свои обязанности перед клиентами и какое качество обслуживания. Что вы 
можете ему предложить?

- RAM - это объем оперативной памяти хоста, 
- indoes - кол-во файловых дескрипторов, которые хранят информацию о файлах системыи, 
- CPUla - загрузка процессора

Для того что бы привести метрики в понятный вид, нужно утвердить SLA в рамках которого будут указаны SLO для тех метрик. 
После этого будет видна разница значений SLO и SLI. Если значения SLI метрики не противоречат установленным для нее SLO тогда продукт в норме

Для описанной системы такими индикаторами могут быть:

- доступность системы в процентах;
- время выполнения запрошенной клиентом операции (минимальное, среднее и максимальное)
- допустимый процент ошибок


5. Вашей DevOps команде в этом году не выделили финансирование на построение системы сбора логов. Разработчики в свою 
очередь хотят видеть все ошибки, которые выдают их приложения. Какое решение вы можете предпринять в этой ситуации, 
чтобы разработчики получали ошибки приложения?

Если позволяют политики ИБ, то можно использовать облачные системы сбора логов например Sentry.
Иначе если объем ошибок не большой можно отправлять на почту.

7. Вы, как опытный SRE, сделали мониторинг, куда вывели отображения выполнения SLA=99% по http кодам ответов. 
Вычисляете этот параметр по следующей формуле: summ_2xx_requests/summ_all_requests. Данный параметр не поднимается выше 
70%, но при этом в вашей системе нет кодов ответа 5xx и 4xx. Где у вас ошибка?

30% запросов завершаются с кодами 100-199 (informational) и\или кодами 300-399 (redirectional), в общем случае не являющимися ошибочными. 
Их нужно либо добавить в числитель выражения, либо вычесть из знаменателя.


## Дополнительное задание (со звездочкой*) - необязательно к выполнению

Вы устроились на работу в стартап. На данный момент у вас нет возможности развернуть полноценную систему 
мониторинга, и вы решили самостоятельно написать простой python3-скрипт для сбора основных метрик сервера. Вы, как 
опытный системный-администратор, знаете, что системная информация сервера лежит в директории `/proc`. 
Также, вы знаете, что в системе Linux есть  планировщик задач cron, который может запускать задачи по расписанию.

Суммировав все, вы спроектировали приложение, которое:
- является python3 скриптом
- собирает метрики из папки `/proc`
- складывает метрики в файл 'YY-MM-DD-awesome-monitoring.log' в директорию /var/log 
(YY - год, MM - месяц, DD - день)
- каждый сбор метрик складывается в виде json-строки, в виде:
  + timestamp (временная метка, int, unixtimestamp)
  + metric_1 (метрика 1)
  + metric_2 (метрика 2)
  
     ...
     
  + metric_N (метрика N)
  
- сбор метрик происходит каждую 1 минуту по cron-расписанию

Для успешного выполнения задания нужно привести:

а) работающий код python3-скрипта,

б) конфигурацию cron-расписания,

в) пример верно сформированного 'YY-MM-DD-awesome-monitoring.log', имеющий не менее 5 записей,

P.S.: количество собираемых метрик должно быть не менее 4-х.
P.P.S.: по желанию можно себя не ограничивать только сбором метрик из `/proc`.

---

### Как оформить ДЗ?

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---