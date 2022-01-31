import json
from vk_api.longpoll import VkEventType
from classes.db_orm import session
from classes.vk_class import VkUser
from classes.vk_bot import VkBot
from functions.res_process import response_processing
from functions.req_process import request_processing
from settings import login, vk_token_personal, vk_token_community


if __name__ == '__main__':

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
                        result = response_processing(response, vk_client, bot, event.user_id)
                        session.close()