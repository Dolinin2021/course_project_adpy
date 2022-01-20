import vk_api
from vk_bot import VkBot
from db_orm import session, ban_list


def response_processing(response, vk_user_class_obj, vk_bot_class_obj, user_id):

    photo_list = []
    url = "https://vk.com/id"

    for value in response['items']:
        try:
            if value['id'] not in ban_list:
                photo_info = vk_user_class_obj.photos_get(value['id'], 'profile')
                for info in photo_info:
                    photo_list.append(f"photo{value['id']}_{info['photo_id']}")

                if len(photo_list) == 3:
                    res = VkBot.user_interaction(vk_bot_class_obj, value, user_id, url, photo_list)
                    if res:
                        return

                else:
                    albums_info = vk_user_class_obj.get_albums(value['id'])
                    for album in albums_info:
                        photo_info = vk_user_class_obj.photos_get(value['id'], album['id'])
                        for info in photo_info:
                            photo_list.append(f"photo{value['id']}_{info['photo_id']}")

                        if len(photo_list) == 3:
                            res = VkBot.user_interaction(vk_bot_class_obj, value, user_id, url, photo_list)
                            if res:
                                return

                    else:
                        res = VkBot.user_interaction(vk_bot_class_obj, value, user_id, url, photo_list)
                        if res:
                            return

        except vk_api.exceptions.ApiError:
            ...
        finally:
            session.commit()