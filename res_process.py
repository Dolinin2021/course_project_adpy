import vk_api


def response_processing(response, vk_class_obj, vk_bot_obj, user_id):

    url = "https://vk.com/id"

    photo_list = []

    for value in response:
        try:
            photo_info = vk_class_obj.photos_get(value['id'])
            # pprint(photo_info)
            for info in photo_info:
                photo_list.append(f"photo{value['id']}_{info['photo_id']}")

            photos = ','.join(photo_list)
            # pprint(photo_list)
            # pprint(photos)

            vk_bot_obj.write_msg(user_id,f"Фамилия: {value['last_name']}\n"
                                         f"Имя: {value['first_name']}\n"
                                         f"Профиль: {url + str(value['id'])}\n",
                          photos)

            photo_list.clear()

        except vk_api.exceptions.ApiError as error_msg:
            # print(error_msg)
            vk_bot_obj.write_msg(user_id, f"Возникла ошибка API VK. \n"
                                         f"Код ошибки и её описание: \n{error_msg}")
