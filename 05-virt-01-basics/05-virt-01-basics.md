### Домашнее задание к занятию "5.1. Введение в виртуализацию. Типы и функции гипервизоров. Обзор рынка вендоров и областей применения."
#### Задача 1
Опишите кратко, как вы поняли: в чем основное отличие полной (аппаратной) виртуализации, паравиртуализации и виртуализации на основе ОС.

```
 - При апаратной виртуализации гипервизор устанавливается на "железо".
 - При паравиртуализации на "железо" устанавливается операционная система, а в ней уже устанавливается приложение для создания и запуска виртуальных машин.
 - При виртуализации на основе ОС на "железо" устанавливается ОС, далее средствами ОС запускается гостевая ОС. В таком случае гостевые ОС могут иметь только ядро аналогичное базовой ОС .
```
#### Задача 2
Выберите один из вариантов использования организации физических серверов, в зависимости от условий использования.

Организация серверов:

- физические сервера,
- паравиртуализация,
- виртуализация уровня ОС.

Условия использования:

- Высоконагруженная база данных, чувствительная к отказу.
- Различные web-приложения.
- Windows системы для использования бухгалтерским отделом.
- Системы, выполняющие высокопроизводительные расчеты на GPU.

Опишите, почему вы выбрали к каждому целевому использованию такую организацию.

| Условия | Организация серверов    | Почему                                                                                                                                                                                                                                                    |
| --- |-------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Высоконагруженная база данных, чувствительная к отказу | физические сервера      | Для высоконагруженной СУБД требуется максимум ресурсов хоста, присутствие соседей которые могут их отобрать нежелательно. Но в таком случае требуется обеспечить резервирование СУБД путем создания кластера средствами СУБД на нескольких физ. серверах. |
| Различные web-приложения | виртуализация уровня ОС | Виртуализация ОС подходит лучше всего, тк часто для этого используются контейнеры                                                                                                                                                                         |
| Windows системы для использования бухгалтерским отделом | паравиртуализация       | Виртуализация поможет системе быть более отказоустойчивой, из предложенных вариантов для Windows возможна только паравиртуализация.                                                                                                                       |
| Системы, выполняющие высокопроизводительные расчеты на GPU | виртуализация уровня ОС | виртуализация GPU может потребоваться в проектах для ML, из предложенных видов виртуализации для GPU возможна только виртуализация средствами ОС                                                                                                          |

#### Задача 3
Выберите подходящую систему управления виртуализацией для предложенного сценария. Детально опишите ваш выбор.

Сценарии:

1. 100 виртуальных машин на базе Linux и Windows, общие задачи, нет особых требований. Преимущественно Windows based инфраструктура, требуется реализация программных балансировщиков нагрузки, репликации данных и автоматизированного механизма создания резервных копий.
```
Hyper-V, vSphere(ESXi). Хорошо поддерживают виртуальные машины с Windows и Linux, есть возможность объединять хосты в кластер, что необходимо для работы 100 виртуальных машин.
```
2. Требуется наиболее производительное бесплатное open source решение для виртуализации небольшой (20-30 серверов) инфраструктуры на базе Linux и Windows виртуальных машин.
```
Proxmox в режиме KVM: open source решение, хорошо поддерживает Linux и Windows гостевые ОС.
```
3. Необходимо бесплатное, максимально совместимое и производительное решение для виртуализации Windows инфраструктуры.
```
Hyper-V, максимально совместим c Windows гостевыми ОС, гипервизор бесплатен.
```
4. Необходимо рабочее окружение для тестирования программного продукта на нескольких дистрибутивах Linux.
```
Virlual Box с использованием Vagrant
```
#### Задача 4
Опишите возможные проблемы и недостатки гетерогенной среды виртуализации (использования нескольких систем управления виртуализацией одновременно) и что необходимо сделать для минимизации этих рисков и проблем. Если бы у вас был выбор, то создавали бы вы гетерогенную среду или нет? Мотивируйте ваш ответ примерами.
```
Возможные проблемы и недостатки гетерогенной среды виртуализации:
- необходимо наличие специалистов умеющих обслуживать разные системы виртуализации;
- невозможность максимально утилизировать "железо" тк нет единого пула ресурсов;


Действия для минимизации рисков и проблем:
- если гетерогенность не оправдана, то рассмотреть возможность отказа от нее;
- если нет возможности уйти от гетерогенности, то часть инфраструктуры можно перенести на IaaS;


Я бы предпочел работать в единой среде. Небольшие выгоды в цене и производительности при обслуживании разных сред виртуализации ведут к большим издержкам в процессе эксплуатации.
```