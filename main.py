import json
from vk_api.longpoll import VkEventType
from vk_class import VkUser
from vk_bot import VkBot
from res_process import response_processing
from req_process import request_processing


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

    for event in bot.longpoll_listen():

        if event.type == VkEventType.MESSAGE_NEW:

            if event.to_me:
                request = event.text

                if request == event.text:

                    response = request_processing(request, vk_client, bot, event.user_id)

                    if response:
                        result = response_processing(response, vk_client, bot, event.user_id, request)