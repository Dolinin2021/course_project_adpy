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


    for event in bot.longpoll_listen():

        url = "https://vk.com/id"

        if event.type == VkEventType.MESSAGE_NEW:

            if event.to_me:
                request = event.text

                if request == "Привет":
                    search = vk_client.users_get(event.user_id)
                    for name in search:
                        bot.write_msg(event.user_id, f"Привет, {name['first_name']}! Хочешь познакомиться?")

                elif request == "Да":
                    bot.write_msg(event.user_id, "Возраст (от):")
                elif request == "18" :
                    vk_client.age_from = "18"
                    bot.write_msg(event.user_id, "Возраст (до):")

                elif request == "100":
                    vk_client.age_do = "100"
                    bot.write_msg(event.user_id, "Пол: \n0 - любой,\n"
                                                 "1 - женский,\n"
                                                 "2 - мужской\n")
                elif request == "0":
                    vk_client.sex = "0"
                elif request == "1":
                    vk_client.sex = "1"
                elif request == "2" and vk_client.status is None:
                    vk_client.sex = "2"
                    bot.write_msg(event.user_id, "Введите название города:")

                elif request == "Москва":
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
                    response = vk_client.users_search(vk_client.age_from, vk_client.age_do, vk_client.sex, vk_client.hometown, vk_client.status, vk_client.count)

                    for value in response:
                        owner_id = vk_client.users_get(value['id'])

                        for id in owner_id:
                            photo_info = vk_client.photos_get(id['id'])

                        bot.write_msg(event.user_id, f"Фамилия: {value['last_name']}\n"
                                                     f"Имя: {value['first_name']}\n"
                                                     f"Профиль: {url+str(value['id'])}\n"
                                                     f"Фото данного пользователя:")

                # elif request == 'get countries':
                #     bot.write_msg(event.user_id, f"{get_countries()}")


                elif request == "Пока":
                    bot.write_msg(event.user_id, "До встречи!")
                else:
                    bot.write_msg(event.user_id, "Не поняла вашего ответа...\n "
                                                 "Давайте начнём сначала!")
