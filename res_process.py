import vk_api
from pprint import pprint


def response_processing(response, vk_user_class_obj, vk_bot_class_obj, user_id):

    url = "https://vk.com/id"

    photo_list = []
    current_user_id_set = set()

    for value in response:
        try:
            with open("user_id.txt", "r") as file:
                file_user_id = file.readlines()
            print(file_user_id)

            if int(value['id']) not in file_user_id:
                print('False')
                current_user_id_set.add(value['id'])
                print(current_user_id_set)
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
                            break
                    else:
                        photos = ','.join(photo_list[:3])
                        vk_bot_class_obj.write_msg(user_id, f"Фамилия: {value['last_name']}\n"
                                                      f"Имя: {value['first_name']}\n"
                                                      f"Профиль: {url + str(value['id'])}\n", photos)
                        photo_list.clear()
            else:
                print('True')
                continue

        except vk_api.exceptions.ApiError as error_msg:
                # print(error_msg)
                vk_bot_class_obj.write_msg(user_id, f"Возникла ошибка API VK. \n"
                                              f"Код ошибки и её описание: \n{error_msg}")
        finally:
            with open("user_id.txt", "w") as file:
                file.writelines("%s\n" % line for line in current_user_id_set)