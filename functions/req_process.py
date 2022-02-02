import re
import json
import vk_api
from classes.db_orm import session, BanList, FavoriteList, UniqueList, favorite_list, ban_list, unique_list
from functions.favor_list import favorite_of_list


def request_processing(request, vk_user_class_obj, vk_bot_class_obj, user_id):
    """ Функция для обработки запросов.

    :param request: запрос пользователя
    :type request: str

    :param vk_user_class_obj: объект :class:`VkUser`
    :type vk_user_class_obj: class 'VkUser'

    :param vk_bot_class_obj: объект :class:`VkBot`
    :type vk_bot_class_obj: class 'VkBot'

    :param user_id: id пользователя
    :type user_id: int

    :except vk_api.exceptions.ApiError: исключения VK API
    Ссылка на официальную документацию: https://vk.com/dev/errors

    """

    HELP = """
    Для того, чтобы найти человека через наш сервис, 
    Вам необходимо ввести следующие команды:
    
    1) Запуск - команда для вывода приветствия,
    
    2) Мой id: <id-пользователя> - команда для ввода имени пользователя или его id в ВК, для которого мы ищем пару,
    
    3) Справка - команда для вывода справки,

    4) Возраст от <число> до <число> лет - команда для ввода возраста (от 18 до 80 лет включительно),

    5) Пол: <число> - команда для ввода пола, где <число>:
    0 — любой пол,
    1 — женский пол,
    2 — мужской пол.

    6) Страна: <название страны> - команда для ввода страны,

    7) Город: <название города> - команда для ввода города,

    8) Семейное положение: <число> - команда для ввода семейного положения, где <число>:
    1 — не женат (не замужем),
    2 — встречается,
    3 — помолвлен(-а),
    4 — женат (замужем),
    5 — всё сложно,
    6 — в активном поиске,
    7 — влюблен(-а),
    8 — в гражданском браке.

    Для того, чтобы корректно работал поиск пользователей по заданным параметрам, необходимо ввести все параметры.

    Введите команду 'Поиск' для выполнения запроса по заданным параметрам.

    Введите команду 'Избранное', чтобы увидеть список понравившихся пользователей.

    Введите команду 'Выход', чтобы выйти из программы.
    """

    pattern_id = r"Мой id:\s*\S*\s*"
    pattern_age = r"Возраст от\s*\d*\s*до\s*\d*\s*лет"
    pattern_sex = r"Пол:\s*\d+"

    pattern_country = r"Страна:\s*\D+"
    pattern_hometown = r"Город:\s*\D+"
    pattern_status = r"Семейное положение:\s*\d+"

    id_list = re.search(pattern_id, request, re.I)
    age_list = re.search(pattern_age, request, re.I)
    sex_list = re.search(pattern_sex, request, re.I)

    country_list = re.search(pattern_country, request, re.I)
    hometown_list = re.search(pattern_hometown, request, re.I)
    status_list = re.search(pattern_status, request, re.I)

    if request == "Запуск":
        vk_bot_class_obj.write_msg(user_id, "Вас приветствует чат-бот VKinder! \n"
                                            "Желаете воспользоваться нашим сервисом для знакомств? \n"
                                            "Для начала введите свой id или screen_name, \n"
                                            "используя следующий формат: \n"
                                            "Мой id: <id-пользователя>")

    elif request == "Справка":
        vk_bot_class_obj.write_msg(user_id, HELP)

    elif request == "Да" or request == "Нет" or request == "Стоп" or request == "Продолжить":
        ...

    elif request == "Избранное":
        favorite_of_list(vk_user_class_obj, vk_bot_class_obj, user_id)

    elif request == "Выход":
        vk_bot_class_obj.write_msg(user_id, "До встречи!")
        session.query(UniqueList).delete()
        session.query(BanList).delete()
        session.query(FavoriteList).delete()
        session.commit()
        session.close()
        unique_list.clear()
        favorite_list.clear()
        ban_list.clear()
        exit()

    elif id_list:
        pattern_str_id = r"[^Мой id:\s]\S*\s*"
        str_id_list = re.findall(pattern_str_id, id_list[0])
        if str_id_list:
            vk_user_class_obj.user_ids = str_id_list[0]
            try:
                search = vk_user_class_obj.users_get(vk_user_class_obj.user_ids)
                if search:
                    for name in search:
                        vk_bot_class_obj.write_msg(user_id,
                                                   f"{name['first_name']}, индентификатор пользователя задан корректно, теперь введите слово 'Справка', "
                                                   f"чтобы вывелось окно с инструкцией по использованию программы. ")
                else:
                    vk_bot_class_obj.write_msg(user_id, "Ничего не найдено, попробуйте ещё раз.")
            except vk_api.exceptions.ApiError:
                ...

    elif age_list:
        pattern_int_age = r"[\d]+[\d]+"
        age_int_list = re.findall(pattern_int_age, age_list[0])
        age_from = int(age_int_list[0])
        age_do = int(age_int_list[1])
        if age_int_list and age_from >= 18 and age_do <= 80 and age_do > age_from:
            vk_user_class_obj.age_from = age_from
            vk_user_class_obj.age_do = age_do
            vk_bot_class_obj.write_msg(user_id, "Возраст задан корректно, теперь введите пол. \n"
                                                "Шаблон: Пол: <число>, где <число>: \n"
                                                "0 — любой пол, \n"
                                                "1 — женский пол, \n"
                                                "2 — мужской пол.")
        else:
            vk_bot_class_obj.write_msg(user_id,
                                       "Ошибка: следует ввводить возраст в промежутке от 18 до 80 лет включительно. Попробуйте ещё раз.")

    elif sex_list:
        pattern_int_sex = r"\d+"
        sex_int_list = re.search(pattern_int_sex, sex_list[0])
        sex = int(sex_int_list[0])
        if sex_int_list and sex >= 0 and sex <= 2:
            vk_user_class_obj.sex = sex
            vk_bot_class_obj.write_msg(user_id, "Пол задан корректно, теперь введите название страны. \n"
                                                "Шаблон: Страна: <название страны> \n"
                                                "При неправильно введённом значении поиск не сработает.")
        else:
            vk_bot_class_obj.write_msg(user_id,
                                       "Ошибка: следует ввводить пол в промежутке от 0 до 2 включительно. Попробуйте ещё раз. \n")

    elif country_list:
        pattern_name_country = r"[^Страна:\s]\D+"
        # Иногда регулярное выражение не находит первую букву
        # и вместо слово 'Россия' получается слово 'оссия'
        # поэтому здесь не используется флаг re.IGNORECASE
        country_name = re.search(pattern_name_country, country_list[0])
        if country_name:
            with open('countries.json', 'r', encoding='utf-8') as file_obj:
                data_countries = json.load(file_obj)
            try:
                for data in data_countries:
                    for key, value in data.items():
                        if country_name[0] in key:
                            vk_user_class_obj.country_id = value
                            vk_bot_class_obj.write_msg(user_id,
                                                       "Страна задана верно. теперь введите название города. \n"
                                                       "Шаблон: Город: <название города> \n"
                                                       "При неправильно введённом значении поиск ничего не найдёт.")
            except TypeError:
                vk_bot_class_obj.write_msg(user_id, "Страна не найдена. Попробуйте ещё раз")

    elif hometown_list:
        pattern_name_hometown = r"[^Город:\s]\D+"
        hometown_name = re.search(pattern_name_hometown, hometown_list[0], re.I)
        if hometown_name:
            vk_user_class_obj.hometown = hometown_name[0]
            vk_bot_class_obj.write_msg(user_id, "Город задан верно, теперь введите семейное положение. \n"
                                                "Шаблон: Семейное положение: <число>, где <число>: \n"
                                                "1 — не женат (не замужем),\n"
                                                "2 — встречается,\n"
                                                "3 — помолвлен(-а),\n"
                                                "4 — женат (замужем),\n"
                                                "5 — всё сложно,\n"
                                                "6 — в активном поиске,\n"
                                                "7 — влюблен(-а),\n"
                                                "8 — в гражданском браке \n")

    elif status_list:
        pattern_int_status = r"\d+"
        status_int_list = re.search(pattern_int_status, status_list[0])
        status = int(status_int_list[0])
        if status_int_list and status >= 1 and status <= 8:
            vk_user_class_obj.status = status
            vk_bot_class_obj.write_msg(user_id, "Семейное положение задано верно,"
                                                "теперь введите команду 'Поиск'.")
        else:
            vk_bot_class_obj.write_msg(user_id,
                                       "Ошибка: следует ввводить семейное положение в промежутке от 1 до 8 включительно. Попробуйте ещё раз.")

    elif request == "Поиск":
        if vk_user_class_obj.age_from and vk_user_class_obj.age_do and vk_user_class_obj.sex and \
                vk_user_class_obj.hometown and vk_user_class_obj.status:

            vk_bot_class_obj.write_msg(user_id, "Все параметры заданы верно.")

            response = vk_user_class_obj.users_search(vk_user_class_obj.age_from,
                                                      vk_user_class_obj.age_do,
                                                      vk_user_class_obj.sex,
                                                      vk_user_class_obj.country_id,
                                                      vk_user_class_obj.hometown,
                                                      vk_user_class_obj.status)

            vk_bot_class_obj.write_msg(user_id, f"По Вашему запросу найдено {response['count']} пользователей. \n")

            if response['items'] == []:
                vk_bot_class_obj.write_msg(user_id, "По Вашему запросу ничего не найдено.")
                return

            return response

        else:
            vk_bot_class_obj.write_msg(user_id,
                                       "Ошибка: недостаточно параметров для поиска. Проверьте ввдённые параметры и попробуйте ещё раз.")

    else:
        vk_bot_class_obj.write_msg(user_id, "Неправильный ввод команды. Попробуйте ещё раз.")