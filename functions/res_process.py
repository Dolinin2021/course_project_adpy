import vk_api
import sqlalchemy.exc
import psycopg2.errors
from classes.db_orm import session, UniqueList, unique_list, ban_list


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

    :exception psycopg2.errors.UniqueViolation: повторяющееся значение ключа нарушает ограничение уникальности

    :exception sqlalchemy.exc.IntegrityError: повторяющееся значение ключа нарушает ограничение уникальности

    :exception sqlalchemy.exc.PendingRollbackError: не удалось выполнить транзакцию, её необходимо отменить,
                                            чтобы продолжить.

    """

    photo_list = []
    url = "https://vk.com/id"

    for value in response['items']:
        try:
            if value['id'] not in ban_list and value['id'] not in unique_list:

                unique = UniqueList(id=value['id'])
                unique_list.append(value['id'])
                session.add(unique)

                photo_info = vk_user_class_obj.photos_get(value['id'], 'profile')
                for info in photo_info:
                    photo_list.append(f"photo{value['id']}_{info['photo_id']}")

                if len(photo_list) == 3:
                    # Если длина списка фотографий равна 3, то выведи в чат результат выполнения запроса.
                    break_out_flag = vk_bot_class_obj.query_result(value, user_id, url, photo_list)
                    # Если пользователь ввёл команду 'Стоп', останови цикл.
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
        except psycopg2.errors.UniqueViolation:
            ...
        except sqlalchemy.exc.IntegrityError:
            ...
        except sqlalchemy.exc.PendingRollbackError:
            ...