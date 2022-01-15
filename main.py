import re
import json
from vk_api.longpoll import VkEventType
from pprint import pprint
from vk_class import VkUser
from vk_bot import VkBot
from res_process import response_processing


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


if __name__ == '__main__':

    with open('vk_token_personal.txt', 'r', encoding='utf-8') as file_obj:
        vk_token_personal = file_obj.read().strip()

    with open('vk_token_com.txt', 'r', encoding='utf-8') as vk_file:
        vk_token_community = vk_file.read().strip()

    with open('vk_login.txt', 'r', encoding='utf-8') as file_obj:
        login = file_obj.read().strip()


    vk_client = VkUser(login, vk_token_personal)

    bot = VkBot(login, vk_token_community)

    country = VkUser.get_countries(login, vk_token_personal)

    with open('countries.json', 'w', encoding='utf-8') as file_obj:
        json.dump(country, file_obj, ensure_ascii=False, indent=4)

    pattern_age = r"Возраст от\s*\d*\s*до\s*\d*\s*лет"
    pattern_sex = r"Пол:\s*\d{1}"

    pattern_country = r"Страна:\s\D+\S"
    pattern_hometown = r"Город:\s\D+\S"

    pattern_status = r"Семейное положение:\s*\d{1}"
    pattern_count_users = r"Количество запрашиваемых пользователей:\s*\d+"

    for event in bot.longpoll_listen():

        url = "https://vk.com/id"

        if event.type == VkEventType.MESSAGE_NEW:

            if event.to_me:
                request = event.text

                # задание параметров через регулярные выражения
                if request == event.text:

                    if request == "Запуск":
                        bot.write_msg(event.user_id, f"Вас приветствует чат-бот VKinder! "
                                                     f"Желаете воспользоваться нашим сервисом для знакомств? \n"
                                                     f"Введите слово 'Да', чтобы продолжить... ")

                    if request == "Да":
                        bot.write_msg(event.user_id, HELP)

                    if request == "Пока":
                        bot.write_msg(event.user_id, "До встречи!")


                    age_list = re.search(pattern_age, request, re.I)
                    if age_list:
                        pattern_int_age = r"[\d]+[\d]+"
                        age_int_list = re.findall(pattern_int_age, age_list[0])
                        if age_int_list:
                            vk_client.age_from = age_int_list[0]
                            vk_client.age_do = age_int_list[1]
                            # print(vk_client.age_from)
                            # print(vk_client.age_do)
                            bot.write_msg(event.user_id, "Возраст задан корректно, теперь введите пол. \n"
                                                         "Шаблон: Пол: <число>, где <число>: \n"
                                                         "0 — любой пол, \n"
                                                         "1 — женский пол, \n"
                                                         "2 — мужской пол.")


                    sex_list = re.search(pattern_sex, request, re.I)
                    if sex_list:
                        pattern_int_sex = r"\d{1}"
                        sex_int_list = re.search(pattern_int_sex, sex_list[0])
                        if sex_int_list:
                            vk_client.sex = sex_int_list[0]
                            # print(vk_client.sex)
                            bot.write_msg(event.user_id, "Пол задан корректно, теперь введите название страны. \n"
                                                         "Шаблон: Страна: <название страны>")


                    country_list = re.search(pattern_country, request, re.I)
                    if country_list:
                        pattern_name_country = r"[^Страна:\s]\D+\S"
                        country_name = re.search(pattern_name_country, country_list[0], re.I)
                        with open('countries.json', 'r', encoding='utf-8') as file_obj:
                            data_countries = json.load(file_obj)

                        for data in data_countries:
                            for key, value in data.items():
                                if country_name[0] in key:
                                    vk_client.country_id = value
                                    # print(vk_client.country_id)
                                    bot.write_msg(event.user_id, "Страна задана верно. теперь введите название города. \n"
                                                                 "Шаблон: Город: <название города>")


                    hometown_list = re.search(pattern_hometown, request, re.I)
                    if hometown_list:
                        pattern_name_hometown = r"[^Город:\s]\D+\S"
                        hometown_name = re.search(pattern_name_hometown, hometown_list[0], re.I)
                        vk_client.hometown = hometown_name[0]
                        # print(vk_client.hometown)
                        bot.write_msg(event.user_id, "Город задан верно, теперь введите семейное положение. \n"
                                                     "Шаблон: Семейное положение: <число>, где <число>: \n"
                                                     "1 — не женат (не замужем),\n"
                                                     "2 — встречается,\n"
                                                     "3 — помолвлен(-а),\n"
                                                     "4 — женат (замужем),\n"
                                                     "5 — всё сложно,\n"
                                                     "6 — в активном поиске,\n"
                                                     "7 — влюблен(-а),\n"
                                                     "8 — в гражданском браке")


                    status_list = re.search(pattern_status, request, re.I)
                    if status_list:
                        pattern_int_status = r"\d{1}"
                        status_int_list = re.search(pattern_int_status, status_list[0])
                        if status_int_list:
                            vk_client.status = status_int_list[0]
                            # print(vk_client.status)
                            bot.write_msg(event.user_id, "Семейное положение задано верно, \n"
                                                         "теперь введите количество запрашиваемых пользователей. \n"
                                                         "Шаблон: Количество запрашиваемых пользователей: <число>")


                    count_list = re.search(pattern_count_users, request, re.I)
                    if count_list:
                        pattern_int_count = r"\d+"
                        count_int_list = re.search(pattern_int_count, count_list[0])
                        if count_int_list:
                            vk_client.count = count_int_list[0]
                            # print(vk_client.count)
                            bot.write_msg(event.user_id, "Количество пользователей задано верно. \n"
                                                         "Результат:")

                            response = vk_client.users_search(vk_client.age_from, vk_client.age_do, vk_client.sex,
                                                              vk_client.country_id, vk_client.hometown,
                                                              vk_client.status, vk_client.count)
                            # pprint(response)

                            result = response_processing(response, vk_client, bot, event.user_id)
