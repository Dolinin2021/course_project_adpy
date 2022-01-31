## Курсовая работа "VKinder"

Курсовой проект представляет собой приложение для знакомств - чат-бот VKinder. Он обеспечивает простой интерфейс для выбора понравившегося человека.

Поиск подходящих людей осуществляется на основании информации о пользователе из VK:
- возраст,
- пол,
- страна,
- город,
- семейное положение.


## Входные данные
Имя пользователя или его id в ВК, для которого мы ищем пару.


## Функциональность
1. У тех людей, которые подошли по требованиям пользователю, бот получает топ-3 популярных фотографии профиля и отправляет их пользователю в чат со ссылкой на найденного человека. Популярность определяется по количеству лайков и комментариев.
2. Люди не повторяются при повторном поиске.
3. Есть возможность добавить человека в избранный список, используя БД.
4. Есть возможность добавить человека в черный список чтобы он больше не попадался при поиске, используя БД.
5. Результат программы записывается в БД.


## Технические замечания
1. Программа декомпозирована на функции/классы/модули/пакеты.
2. Пакет `classes` содержит классы для работы с аккаунтом ВКонтакте, ботом Вконтакте, ORM sqlalchemy.
3. Пакет `functions` содержит функции для обработки входящих запросов пользователя, ответа сервера, а также функцию для добавления пользователя в список 'Избранное'.
4. Файл с настройками `settings.py` находится в корневом каталоге проекта.
5. Все зависимости указаны в файле `requiremеnts.txt`, он также находится в корневом каталоге проекта.
6. Все функции, классы и методы имеют свою документацию.


## Настройка проекта
1. Установить все пакеты из файла `requirements.txt` с помощью команды `pip install -r requirements.txt`
2. Получить ключ доступа (токен) пользователя Вконтакте.
3. Получить ключ доступа (токен) сообщества Вконтакте.
4. Перед запуском заполнить все параметры в файле `settings.py`, подробнее в документации к файлу.


## Руководство пользователя

Для того, чтобы найти нужных людей, необходимо ввести следующие команды:

1.`Возраст от <число> до <число> лет` - команда для ввода возраста (от 18 до 80 лет включительно),

2.`Пол: <число>` - команда для ввода пола, где `<число>`: \
0 — любой пол,\
1 — женский пол, \
2 — мужской пол. 

3.`Страна: <название страны>` - команда для ввода страны,

4.`Город: <название города>` - команда для ввода города,

5.`Семейное положение: <число>` - команда для ввода семейного положения, где `<число>`: \
1 — не женат (не замужем), \
2 — встречается, \
3 — помолвлен(-а), \
4 — женат (замужем), \
5 — всё сложно, \
6 — в активном поиске, \
7 — влюблен(-а), \
8 — в гражданском браке.

Для того, чтобы корректно работал поиск пользователей по заданным параметрам, необходимо ввести все параметры.

Введите команду `Поиск` для выполнения запроса по заданным параметрам.

Введите команду `Избранное`, чтобы увидеть список понравившихся пользователей.

Введите команду `Выход`, чтобы выйти из программы.

## Скриншоты

![screen](https://user-images.githubusercontent.com/89892788/151781655-ae47ca5a-d59e-4d0a-b6c6-7941474468f0.png)

![screen_2](https://user-images.githubusercontent.com/89892788/151815629-caf47ff5-e782-4501-a80a-179b0df3d3d8.png)