import re
import json
import vk_api
from vk_api.longpoll import VkEventType
from pprint import pprint
from vk_class import VkUser
from vk_bot import VkBot


def get_countries(need_all=1):
    country_list = []
    response = vk.database.getCountries(need_all=need_all)
    for value in response['items']:
        country_dict = {
            value['title']: value['id']
        }
        country_list.append(country_dict)
    # pprint(country_list)
    return country_list


HELP = """
Для того, чтобы найти человека через наш сервис, Вам необходимо ввести команды в следующем шаблоне и последовательности:
1) Возраст от <число> до <число> лет - команда для задания параметров возраста,
2) Установить пол <число> - команда для задания параметра пола """


if __name__ == '__main__':

    with open('vk_token_personal.txt', 'r', encoding='utf-8') as file_obj:
        vk_token_personal = file_obj.read().strip()

    with open('vk_token_com.txt', 'r', encoding='utf-8') as vk_file:
        vk_token_community = vk_file.read().strip()

    with open('vk_login.txt', 'r', encoding='utf-8') as file_obj:
        login = file_obj.read().strip()


    vk_client = VkUser(login, vk_token_personal)

    bot = VkBot(login, vk_token_community)


    vk_session = vk_api.VkApi(login=login, token=vk_token_personal)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
    vk = vk_session.get_api()


    country = get_countries()

    with open('countries.json', 'w', encoding='utf-8') as file_obj:
        json.dump(country, file_obj, ensure_ascii=False, indent=4)

    pattern_age = "Возраст от\s*\d*\s*до\s*\d*\s*лет"
    pattern_sex = "Установить пол\s*\d{1}"



    for event in bot.longpoll_listen():

        url = "https://vk.com/id"

        if event.type == VkEventType.MESSAGE_NEW:

            if event.to_me:
                request = event.text

                if request == "Запуск":
                    bot.write_msg(event.user_id, f"Вас приветствует чат-бот VKinder! "
                                                 f"Желаете воспользоваться нашим сервисом для знакомств? "
                                                 f"Введите слово Да, чтобы продолжить... ")

                elif request == "Да":
                    bot.write_msg(event.user_id, HELP)

                # elif request == "25":
                #     vk_client.age_from = int(request)
                #     if vk_client.age_from >= 18 and vk_client.age_from <= 50:
                #         bot.write_msg(event.user_id, "Возраст (до):")
                #     else:
                #         bot.write_msg(event.user_id, "Вы нарушили допустимый диапазон от 18 до 50 лет. Попробуйте ещё раз.")

                # elif request == "100":
                #     vk_client.age_do = int(request)
                #     if vk_client.age_do >= 18 and vk_client.age_do <= 50:
                #         bot.write_msg(event.user_id, "Пол: \n0 - любой,\n"
                #                                      "1 - женский,\n"
                #                                      "2 - мужской\n")
                #     else:
                #         bot.write_msg(event.user_id, "Вы нарушили допустимый диапазон от 18 до 50 лет. Попробуйте ещё раз.")

                # задание параметров через регулярные выражения
                elif request == event.text:
                    # print(request)

                    age_list = re.search(pattern_age, request, re.I)
                    if age_list:
                        # print(age_list[0])
                        # bot.write_msg(event.user_id, age_list[0])
                        pattern_int_age = r"[\d]+[\d]+"
                        age_int_list = re.findall(pattern_int_age, request)
                        if age_int_list:
                            # print(age_int_list[0:2])
                            vk_client.age_from = age_int_list[0]
                            vk_client.age_do = age_int_list[1]
                            print(vk_client.age_from)
                            print(vk_client.age_do)
                            bot.write_msg(event.user_id, "Возраст задан корректно, теперь задайте параметр пола.")

                    sex_list = re.search(pattern_sex, request, re.I)
                    if sex_list:
                        # print(sex_list[0])
                        # bot.write_msg(event.user_id, sex_list[0])
                        pattern_int_sex = r"\d{1}"
                        sex_int_list = re.search(pattern_int_sex, request)
                        if sex_int_list:
                            # print(sex_int_list[0])
                            vk_client.sex = sex_int_list
                            print(vk_client.sex)
                            bot.write_msg(event.user_id, "Пол задан корректно, теперь задайте параметр страны.")


                elif request == "0":
                    vk_client.sex = int(request)
                elif request == "1":
                    vk_client.sex = int(request)
                elif request == "2" and vk_client.status is None:
                    vk_client.sex = int(request)
                    bot.write_msg(event.user_id, "Введите название страны:")

                elif request == "Беларусь":
                    with open('countries.json', 'r', encoding='utf-8') as file_obj:
                        data_countries = json.load(file_obj)
                    # pprint(data_countries)

                    for data in data_countries:
                        for key, value in data.items():
                            if request in key:
                                vk_client.country_id = value
                    bot.write_msg(event.user_id, "Введите название города:")


                elif request == "Минск":
                    vk_client.hometown = request
                    bot.write_msg(event.user_id, "Семейное положение:\n"
                                                 "1 — не женат (не замужем),\n"
                                                 "2 — встречается,\n"
                                                 "3 — помолвлен(-а),\n"
                                                 "4 — женат (замужем),\n"
                                                 "5 — всё сложно,\n"
                                                 "6 — в активном поиске,\n"
                                                 "7 — влюблен(-а),\n"
                                                 "8 — в гражданском браке\n")

                elif request == "не женат":
                    vk_client.status = "1"
                    bot.write_msg(event.user_id, "Введите количество запрашиваемых пользователей:\n")
                elif request == "5":
                    vk_client.count = "5"
                    response = vk_client.users_search(vk_client.age_from, vk_client.age_do, vk_client.sex, vk_client.country_id, vk_client.hometown, vk_client.status, vk_client.count)
                    pprint(response)
                    for value in response:
                        owner_id = vk_client.users_get(value['id'])
                        for id in owner_id:
                            # photo_info = vk_client.photos_get(id['id'])
                            bot.write_msg(event.user_id, f"Фамилия: {value['last_name']}\n"
                                                         f"Имя: {value['first_name']}\n"
                                                         f"Профиль: {url+str(value['id'])}\n"
                                                         f"Фото данного пользователя:")


                elif request == "Пока":
                    bot.write_msg(event.user_id, "До встречи!")
                else:
                    bot.write_msg(event.user_id, "Не поняла вашего ответа...\n "
                                                 "Давайте начнём сначала!")
