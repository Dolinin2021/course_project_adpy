from db_orm import favorite_list
from vk_bot import VkBot


def favorite_of_list(vk_user_class_obj, vk_bot_class_obj, user_id):

    photo_list = []
    url = "https://vk.com/id"

    if favorite_list == []:
        vk_bot_class_obj.write_msg(user_id,
                                   "Список пуст. Добавьте кого-нибудь из найденных пользователей в 'Избранное' и попробуйте ещё раз.")

    elif favorite_list:
        vk_bot_class_obj.write_msg(user_id, "Список понравившихся пользователей: \n")
        for id in favorite_list:
            search = vk_user_class_obj.users_get(id)
            for item in search:
                photo_info = vk_user_class_obj.photos_get(item['id'], 'profile')
                for info in photo_info:
                    photo_list.append(f"photo{item['id']}_{info['photo_id']}")

                if len(photo_list) == 3:
                    res = VkBot.user_interaction(vk_bot_class_obj, item, user_id, url, photo_list, False)
                    if res:
                        return

                else:
                    albums_info = vk_user_class_obj.get_albums(item['id'])
                    for album in albums_info:
                        photo_info = vk_user_class_obj.photos_get(item['id'], album['id'])
                        for info in photo_info:
                            photo_list.append(f"photo{item['id']}_{info['photo_id']}")

                        if len(photo_list) == 3:
                            res = VkBot.user_interaction(vk_bot_class_obj, item, user_id, url, photo_list, False)
                            if res:
                                return

                    else:
                        res = VkBot.user_interaction(vk_bot_class_obj, item, user_id, url, photo_list, False)
                        if res:
                            return