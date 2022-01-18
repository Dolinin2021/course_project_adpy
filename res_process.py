import vk_api
from pprint import pprint
from db_orm import Base, Session, engine, BanList, FavoriteList

def response_processing(response, vk_user_class_obj, vk_bot_class_obj, user_id, request=None):

    url = "https://vk.com/id"

    photo_list = []

    Base.metadata.create_all(engine)

    session = Session()

    for value in response:
        try:
            photo_info = vk_user_class_obj.photos_get(value['id'], 'profile')
            # pprint(photo_info)
            for info in photo_info:
                photo_list.append(f"photo{value['id']}_{info['photo_id']}")
            # pprint(photo_list)
            if len(photo_list) == 3:
                photos = ','.join(photo_list)
                # pprint(photo_list)
                # pprint(photos)
                vk_bot_class_obj.write_msg(user_id, f"Фамилия: {value['last_name']}\n"
                                             f"Имя: {value['first_name']}\n"
                                             f"Профиль: {url + str(value['id'])}\n", photos)
                photo_list.clear()

                vk_bot_class_obj.write_msg(user_id, f"Понравился Вам человек? Да\Нет.\n")
                if request == 'Да':
                    favorite = FavoriteList(value['id'])
                    session.add(favorite)

                elif request == 'Нет':
                    ban = BanList(value['id'])
                    session.add(ban)

            else:
                albums_info = vk_user_class_obj.get_albums(value['id'])
                for album in albums_info:
                    photo_info = vk_user_class_obj.photos_get(value['id'], album['id'])
                    # pprint(photo_info)
                    for info in photo_info:
                        photo_list.append(f"photo{value['id']}_{info['photo_id']}")

                    if len(photo_list) == 3:
                        photos = ','.join(photo_list)
                        vk_bot_class_obj.write_msg(user_id, f"Фамилия: {value['last_name']}\n"
                                                      f"Имя: {value['first_name']}\n"
                                                      f"Профиль: {url + str(value['id'])}\n", photos)
                        photo_list.clear()

                        vk_bot_class_obj.write_msg(user_id, f"Понравился Вам человек? Да\Нет.\n")
                        if request == 'Да':
                            favorite = FavoriteList(value['id'])
                            session.add(favorite)

                        elif request == 'Нет':
                            ban = BanList(value['id'])
                            session.add(ban)

                else:
                    photos = ','.join(photo_list[:3])
                    vk_bot_class_obj.write_msg(user_id, f"Фамилия: {value['last_name']}\n"
                                                  f"Имя: {value['first_name']}\n"
                                                  f"Профиль: {url + str(value['id'])}\n", photos)
                    photo_list.clear()

                    vk_bot_class_obj.write_msg(user_id, f"Понравился Вам человек? Да\Нет.\n")
                    if request == 'Да':
                        favorite = FavoriteList(value['id'])
                        session.add(favorite)

                    elif request == 'Нет':
                        ban = BanList(value['id'])
                        session.add(ban)


        except vk_api.exceptions.ApiError as error_msg:
                # print(error_msg)
                vk_bot_class_obj.write_msg(user_id, f"Возникла ошибка API VK. \n"
                                              f"Код ошибки и её описание: \n{error_msg}")
        finally:
            session.commit()
            session.close()