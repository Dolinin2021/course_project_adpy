import vk_api
from db_orm import session, ban_list


def response_processing(response, vk_user_class_obj, vk_bot_class_obj, user_id):
    """ Функция для обработки результатов запроса.

    :param response: результат запроса
    :type response: dict

    :param vk_user_class_obj: объект :class:`VkUser`
    :type vk_user_class_obj: class 'VkUser'

    :param vk_bot_class_obj: объект :class:`VkBot`
    :type vk_bot_class_obj: class 'VkBot'

    :param user_id: id пользователя
    :type user_id: int

    :except vk_api.exceptions.ApiError: исключения VK API
    Ссылка на официальную документацию: https://vk.com/dev/errors

    """

    photo_list = []
    url = "https://vk.com/id"

    for value in response['items']:
        try:
            if value['id'] not in ban_list:
                photo_info = vk_user_class_obj.photos_get(value['id'], 'profile')
                for info in photo_info:
                    photo_list.append(f"photo{value['id']}_{info['photo_id']}")

                if len(photo_list) == 3:
                    break_out_flag = vk_bot_class_obj.query_result(value, user_id, url, photo_list)
                    if break_out_flag:
                        return

                else:
                    albums_info = vk_user_class_obj.get_albums(value['id'])
                    for album in albums_info:
                        photo_info = vk_user_class_obj.photos_get(value['id'], album['id'])
                        for info in photo_info:
                            photo_list.append(f"photo{value['id']}_{info['photo_id']}")

                        if len(photo_list) == 3:
                            break_out_flag = vk_bot_class_obj.query_result(value, user_id, url, photo_list)
                            if break_out_flag:
                                return

                    else:
                        break_out_flag = vk_bot_class_obj.query_result(value, user_id, url, photo_list)
                        if break_out_flag:
                            return

        except vk_api.exceptions.ApiError:
            ...
        finally:
            session.commit()