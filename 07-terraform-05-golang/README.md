# Домашнее задание к занятию "7.5. Основы golang"

С `golang` в рамках курса, мы будем работать не много, поэтому можно использовать любой IDE. 
Но рекомендуем ознакомиться с [GoLand](https://www.jetbrains.com/ru-ru/go/).  

## Задача 1. Установите golang.
1. Воспользуйтесь инструкций с официального сайта: [https://golang.org/](https://golang.org/).
2. Так же для тестирования кода можно использовать песочницу: [https://play.golang.org/](https://play.golang.org/).

## Задача 2. Знакомство с gotour.
У Golang есть обучающая интерактивная консоль [https://tour.golang.org/](https://tour.golang.org/). 
Рекомендуется изучить максимальное количество примеров. В консоли уже написан необходимый код, 
осталось только с ним ознакомиться и поэкспериментировать как написано в инструкции в левой части экрана.  

## Задача 3. Написание кода. 
Цель этого задания закрепить знания о базовом синтаксисе языка. Можно использовать редактор кода 
на своем компьютере, либо использовать песочницу: [https://play.golang.org/](https://play.golang.org/).

1. Напишите программу для перевода метров в футы (1 фут = 0.3048 метр). Можно запросить исходные данные 
у пользователя, а можно статически задать в коде.
Для взаимодействия с пользователем можно использовать функцию `Scanf`

   
  ```commandline
package main

import "fmt"

func ConverterMtoF(m float64) (f float64) {
	f = m * 3.28083989501312
	return f
}

func main() {
	fmt.Print("Введите длину в метрах ")
	var input float64
	fmt.Scanf("%f", &input)

	fmt.Printf("Длина в футах = %v\n", ConverterMtoF(input))
}

go run ./Converter.go 
Введите длину в метрах 20.0
Длина в футах = 65.6167979002624
  ```
 
1. Напишите программу, которая найдет наименьший элемент в любом заданном списке, например:
    ```
    x := []int{48,96,86,68,57,82,63,70,37,34,83,27,19,97,9,17,}
    ```
```commandline
package main

import "fmt"

func main() {

	array := []int{48, 96, 86, 68, 57, 82, 63, 70, 37, 34, 83, 27, 19, 97, 9, 17}
	smallestNumber := array[0]
	for _, element := range array {
		if element < smallestNumber {
			smallestNumber = element

		}
	}
	fmt.Println("Минимальное число = ", smallestNumber)

}

go run ./MinNumber.go
Минимальное число =  9
```
1. Напишите программу, которая выводит числа от 1 до 100, которые делятся на 3. То есть `(3, 6, 9, …)`.
```commandline
package main

import "fmt"

func Devided3() (devidedWithNoReminder []int) {
	for i := 1; i <= 100; i++ {
		if i%3 == 0 {
			devidedWithNoReminder = append(devidedWithNoReminder, i)
		}
	}
	return
}

func main() {
	toPrint := Devided3()
	fmt.Printf("Числа от 1 до 100 которые делятся на 3 без остатка: %v\n", toPrint)
}


go run ./Devided3.go 
Числа от 1 до 100 которые делятся на 3 без остатка: [3 6 9 12 15 18 21 24 27 30 33 36 39 42 45 48 51 54 57 60 63 66 69 72 75 78 81 84 87 90 93 96 99]
```
В виде решения ссылку на код или сам код. 

## Задача 4. Протестировать код (не обязательно).

Создайте тесты для функций из предыдущего задания. 
```commandline
package main

import "testing"

func TestMain(t *testing.T) {
	var v float64
	v = ConverterMtoF(20)
	if v != 65.6167979002624 {
		t.Error("Должно быть 65.6167979002624, получилось ", v)
	}
}

go test Converter.go Converter_test.go 
ok      command-line-arguments  0.002s
```
---

### Как cдавать задание

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---
