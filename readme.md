## Программа для автомата для выдачи продуктов 

## Установка программы

1. `python -m venv venv`
1. windows `.\venv\Scripts\activate` unix `source ./venv/bin/activate`
1. `pip install -r requirements.txt`

## Запуск программы
1. запустить файл interface\main.py

## Добавление новых зависимостей
1. `pip freeze > requirements.txt`

## Замечание
В папке Arduino содержится программный код, который имитирует работу самого автомата(tinkercad). для выдачи продуктов.

В папке Data содержится все возможные данные, такие как данные о продуктах, данные о покупках, данные температуры и влажности воздуха в автомате.

Срок хранения продутов в атомате - от 15 до 30 градусов при влажности от 45 до 60.

у определенных продутов истек срок годности, кончился товар для проверки предупреждений

влажность и температура город Москва