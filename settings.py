""" Файл настроек. Для дальнейшей работы с проектом необходимо заполнить параметры в этом файле.

DATABASE - словарь с параметрами для подключения к базе данных (БД).

Параметры  DATABASE:
    drivername - имя драйвера,
    host - устройство, на котором расположена БД,
    port - порт, используемый для подключения к БД,
    username - имя пользователя-владельца БД,
    password - пароль пользователя,
    database - имя БД.

Ссылка на официальную документацию: https://docs.sqlalchemy.org/en/14/tutorial/engine.html

Файл также хранит данные, необходимые для работы с VK API:
    ключ доступа пользователя (vk_token_personal),
    ключ доступа сообщества (vk_token_community),
    логин пользователя Вконтакте (login).

Ссылка на официальную документацию: https://dev.vk.com/api/access-token/getting-started

"""

DATABASE = {
    'drivername': 'postgresql+psycopg2',
    'host': 'localhost',
    'port': '5432',
    'username': 'ilya',
    'password': '12345',
    'database': 'adpy_course_project'
}

vk_token_personal = ''
vk_token_community = ''
login = ''