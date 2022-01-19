import vk_api
from pprint import pprint
from vk_bot import VkBot
from vk_class import VkUser
from db_orm import session, ban_list, favorite_list
from vk_api.longpoll import VkEventType

def response_processing(response, vk_user_class_obj, vk_bot_class_obj, user_id):

    photo_list = []
    url = "https://vk.com/id"

    for value in response:
        try:
            photo_info = vk_user_class_obj.photos_get(value['id'], 'profile')
            for info in photo_info:
                photo_list.append(f"photo{value['id']}_{info['photo_id']}")
            if len(photo_list) == 3:
                photos = ','.join(photo_list)
                vk_bot_class_obj.write_msg(user_id, f"Фамилия: {value['last_name']}\n"
                                             f"Имя: {value['first_name']}\n"
                                             f"Профиль: {url + str(value['id'])}\n", photos)
                res = VkBot.add_profile_in_list(vk_bot_class_obj, user_id, value['id'])
                photo_list.clear()

            else:
                albums_info = vk_user_class_obj.get_albums(value['id'])
                for album in albums_info:
                    photo_info = vk_user_class_obj.photos_get(value['id'], album['id'])
                    for info in photo_info:
                        photo_list.append(f"photo{value['id']}_{info['photo_id']}")

                    if len(photo_list) == 3:
                        photos = ','.join(photo_list)
                        vk_bot_class_obj.write_msg(user_id, f"Фамилия: {value['last_name']}\n"
                                                      f"Имя: {value['first_name']}\n"
                                                      f"Профиль: {url + str(value['id'])}\n", photos)
                        res = VkBot.add_profile_in_list(vk_bot_class_obj, user_id, value['id'])
                        photo_list.clear()

                else:
                    photos = ','.join(photo_list[:3])
                    vk_bot_class_obj.write_msg(user_id, f"Фамилия: {value['last_name']}\n"
                                                  f"Имя: {value['first_name']}\n"
                                                  f"Профиль: {url + str(value['id'])}\n", photos)
                    res = VkBot.add_profile_in_list(vk_bot_class_obj, user_id, value['id'])
                    photo_list.clear()


        except vk_api.exceptions.ApiError as error_msg:
                # print(error_msg)
                vk_bot_class_obj.write_msg(user_id, f"Возникла ошибка API VK. \n"
                                              f"Код ошибки и её описание: \n{error_msg}")
        finally:
            session.commit()

# def response_processing(response, vk_user_class_obj, vk_bot_class_obj, user_id):
#
#     photo_list = []
#
#     url = "https://vk.com/id"
#
#     try:
#         for value in response:
#             if value['id'] not in ban_list:
#                 VkUser.photo_output(vk_user_class_obj, vk_bot_class_obj, user_id, value, url, photo_list)

        # for event in vk_bot_class_obj.longpoll_listen():
        #     vk_bot_class_obj.write_msg(user_id, "Введите слово 'Избранное', чтобы вывести список понравившихся пользователей. \n")
        #     if event.type == VkEventType.MESSAGE_NEW:
        #
        #         if event.to_me:
        #             request = event.text
        #
        #             if request == "Избранное":
        #                 vk_bot_class_obj.write_msg(user_id, "Список понравившихся пользователей:\n")
        #
        #                 for value in response:
        #                     if value['id'] in favorite_list:
        #                         VkUser.photo_output(vk_user_class_obj, vk_bot_class_obj, user_id, value, url, photo_list)

    # except vk_api.exceptions.ApiError as error_msg:
    #         # print(error_msg)
    #         vk_bot_class_obj.write_msg(user_id, f"Возникла ошибка API VK. \n"
    #                                             f"Код ошибки и её описание: \n{error_msg}")
    # finally:
    #     session.commit()