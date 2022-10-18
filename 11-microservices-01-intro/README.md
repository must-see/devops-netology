# Домашнее задание к занятию "11.01 Введение в микросервисы"

## Задача 1: Интернет Магазин

Руководство крупного интернет магазина у которого постоянно растёт пользовательская база и количество заказов рассматривает возможность переделки своей внутренней ИТ системы на основе микросервисов. 

Вас пригласили в качестве консультанта для оценки целесообразности перехода на микросервисную архитектуру. 

Опишите какие выгоды может получить компания от перехода на микросервисную архитектуру и какие проблемы необходимо будет решить в первую очередь.

Выгоды:
- Возможность быстрого внесения изменений в продукт. Упрощается процедура разработки, тестирования и деплоя, поскольку теперь они затрагивают только микросервис, а не всю монолитную систему целиком.
- Внедрение новых технологий происходит проще. Так как выбор теоретически неограничен, поскольку стэк, используемый одним микросервисом, слабо зависит от стэка другого микросервиса. 
- Устойчивость к ошибкам. Ошибки в одном микросервисе меньше влияют на остальные компоненты системы по сравнению с монолитной архитектурой.
- Эффективное расходование средств за счет более гибкого масштабирования системы. Появляется возможность мониторинга и адаптивного автоматического управления ресурсами для каждого микросервиса в отдельности.


Проблемы:
- Освоить новые компетенции. Микросервисный стэк отличается от монолитного и требует освоения микросервисной архитектуры, паттернов проектирования, используемых технологий.
- Определиться с разбиением функционала на микросервисы.
- Выстроить новые процессы разработки. Собрать команды разработки микросервисов, договориться о спецификациях (контрактах) взаимодействия между микросервисами.
- Подготовить новую инфраструктуру. Рассчитать объем ресурсов и подготовить платформу.
- Разработать эксплуатационные процессы. Continuous Delivery, мониторинг, логирование.

---

### Как оформить ДЗ?

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---