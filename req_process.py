import re
import json


def request_processing(request, vk_class_obj, vk_bot_obj, user_id):

    HELP = """
    Для того, чтобы найти человека через наш сервис, 
    Вам необходимо ввести следующие команды:

    1) Возраст от <число> до <число> лет - команда для ввода возраста,

    2) Пол: <число> - команда для ввода пола, где <число>:
    0 — любой пол,
    1 — женский пол,
    2 — мужской пол.

    3) Страна: <название страны> - команда для ввода страны,

    4) Город: <название города> - команда для ввода города,

    5) Семейное положение: <число> - команда для ввода семейного положения, где <число>:
    1 — не женат (не замужем),
    2 — встречается,
    3 — помолвлен(-а),
    4 — женат (замужем),
    5 — всё сложно,
    6 — в активном поиске,
    7 — влюблен(-а),
    8 — в гражданском браке.

    6) Количество запрашиваемых пользователей: <число> - команда для ввода количества пользователей.
    """

    pattern_age = r"Возраст от\s*\d*\s*до\s*\d*\s*лет"
    pattern_sex = r"Пол:\s*\d{1}"

    pattern_country = r"Страна:\s\D+\S"
    pattern_hometown = r"Город:\s\D+\S"

    pattern_status = r"Семейное положение:\s*\d{1}"
    pattern_count_users = r"Количество запрашиваемых пользователей:\s*\d+"


    age_list = re.search(pattern_age, request, re.I)
    sex_list = re.search(pattern_sex, request, re.I)

    country_list = re.search(pattern_country, request, re.I)
    hometown_list = re.search(pattern_hometown, request, re.I)

    status_list = re.search(pattern_status, request, re.I)
    count_list = re.search(pattern_count_users, request, re.I)


    if request == "Запуск":
        vk_bot_obj.write_msg(user_id, f"Вас приветствует чат-бот VKinder!"
                                     f"Желаете воспользоваться нашим сервисом для знакомств? \n"
                                     f"Введите слово 'Да', чтобы продолжить...")

    elif request == "Да":
        vk_bot_obj.write_msg(user_id, HELP)

    elif request == "Пока":
        vk_bot_obj.write_msg(user_id, "До встречи!")

    elif age_list:
        pattern_int_age = r"[\d]+[\d]+"
        age_int_list = re.findall(pattern_int_age, age_list[0])
        if age_int_list:
            vk_class_obj.age_from = age_int_list[0]
            vk_class_obj.age_do = age_int_list[1]
            # print(vk_client.age_from)
            # print(vk_client.age_do)
            vk_bot_obj.write_msg(user_id, "Возраст задан корректно, теперь введите пол. \n"
                                          "Шаблон: Пол: <число>, где <число>: \n"
                                          "0 — любой пол, \n"
                                          "1 — женский пол, \n"
                                          "2 — мужской пол.")

    elif sex_list:
        pattern_int_sex = r"\d{1}"
        sex_int_list = re.search(pattern_int_sex, sex_list[0])
        if sex_int_list:
            vk_class_obj.sex = sex_int_list[0]
            # print(vk_client.sex)
            vk_bot_obj.write_msg(user_id, "Пол задан корректно, теперь введите название страны. \n"
                                          "Шаблон: Страна: <название страны>")

    elif country_list:
        pattern_name_country = r"[^Страна:\s]\D+\S"
        country_name = re.search(pattern_name_country, country_list[0], re.I)
        with open('countries.json', 'r', encoding='utf-8') as file_obj:
            data_countries = json.load(file_obj)

        for data in data_countries:
            for key, value in data.items():
                if country_name[0] in key:
                    vk_class_obj.country_id = value
                    # print(vk_client.country_id)
                    vk_bot_obj.write_msg(user_id, "Страна задана верно. теперь введите название города. \n"
                                                  "Шаблон: Город: <название города>")

    elif hometown_list:
        pattern_name_hometown = r"[^Город:\s]\D+\S"
        hometown_name = re.search(pattern_name_hometown, hometown_list[0], re.I)
        vk_class_obj.hometown = hometown_name[0]
        # print(vk_client.hometown)
        vk_bot_obj.write_msg(user_id, "Город задан верно, теперь введите семейное положение. \n"
                                      "Шаблон: Семейное положение: <число>, где <число>: \n"
                                      "1 — не женат (не замужем),\n"
                                      "2 — встречается,\n"
                                      "3 — помолвлен(-а),\n"
                                      "4 — женат (замужем),\n"
                                      "5 — всё сложно,\n"
                                      "6 — в активном поиске,\n"
                                      "7 — влюблен(-а),\n"
                                      "8 — в гражданском браке")

    elif status_list:
        pattern_int_status = r"\d{1}"
        status_int_list = re.search(pattern_int_status, status_list[0])
        if status_int_list:
            vk_class_obj.status = status_int_list[0]
            # print(vk_client.status)
            vk_bot_obj.write_msg(user_id, "Семейное положение задано верно, \n"
                                          "теперь введите количество запрашиваемых пользователей. \n"
                                          "Шаблон: Количество запрашиваемых пользователей: <число>")

    elif count_list:
        pattern_int_count = r"\d+"
        count_int_list = re.search(pattern_int_count, count_list[0])
        if count_int_list:
            vk_class_obj.count = count_int_list[0]
            # print(vk_client.count)
            vk_bot_obj.write_msg(user_id, "Количество пользователей задано верно. \n"
                                          "Результат:")

            response = vk_class_obj.users_search(vk_class_obj.age_from, vk_class_obj.age_do, vk_class_obj.sex,
                                              vk_class_obj.country_id, vk_class_obj.hometown,
                                              vk_class_obj.status, vk_class_obj.count)
            return response

    else:
        vk_bot_obj.write_msg(user_id, "Неправильный ввод команды. Попробуйте ещё раз.")