import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randrange
from db_orm import session, BanList, FavoriteList,ban_list, favorite_list


class VkBot:

    def __init__(self, login, token):
        self.login = login
        self.token = token
        self.vk_session = vk_api.VkApi(login=self.login, token=self.token)

    def longpoll_listen(self):
        longpoll = VkLongPoll(self.vk_session, group_id=209853199)
        return longpoll.listen()

    def write_msg(self, user_id, message, photo=None):
        self.vk_session.method('messages.send',
                               {'user_id': user_id, 'message': message, 'attachment': photo, 'random_id': randrange(10 ** 7)})

    @staticmethod
    def add_profile_in_list(vk_bot_class_obj, user_id, profile_id):

        vk_bot_class_obj.write_msg(user_id, "Понравился ли Вам человек? \n")
        vk_bot_class_obj.write_msg(user_id, "Введите команду 'Да', чтобы добавить в 'Избранное'. \n")
        vk_bot_class_obj.write_msg(user_id, "Введите команду 'Нет', чтобы добавить в чёрный список. \n")
        vk_bot_class_obj.write_msg(user_id, "Введите команду 'Продолжить', чтобы пропустить текущего пользователя. \n")
        vk_bot_class_obj.write_msg(user_id, "Введите команду 'Стоп', чтобы остановить поиск. \n")
        vk_bot_class_obj.write_msg(user_id, "Если текущий поиск окончен, введите команду 'Запуск', чтобы начать новый поиск.")

        for event in vk_bot_class_obj.longpoll_listen():
            if event.type == VkEventType.MESSAGE_NEW:

                if event.to_me:
                    request = event.text

                    if request == "Да":
                        favorite = FavoriteList(id=profile_id)
                        favorite_list.append(profile_id)
                        session.add(favorite)
                        break

                    elif request == "Нет":
                        ban = BanList(id=profile_id)
                        ban_list.append(profile_id)
                        session.add(ban)
                        break

                    elif request == "Продолжить":
                        break

                    elif request == "Стоп":
                        vk_bot_class_obj.write_msg(user_id, "Поиск остановлен. \n"
                                                            "Чтобы начать новый поиск, введите команду 'Запуск'. \n"
                                                            "Чтобы увидеть понравившихся пользователей, введите команду 'Избранное'. \n"
                                                            "Чтобы выйти из программы, введите команду 'Выход'.")
                        break_out_flag = True
                        return break_out_flag

                    else:
                        vk_bot_class_obj.write_msg(user_id, "Неверная команда. Попробуйте ещё раз.")

    @staticmethod
    def user_interaction(vk_bot_class_obj, value, user_id, url, list_name, start_function_adding_profile=True):
        photos = ','.join(list_name[:3])
        vk_bot_class_obj.write_msg(user_id, f"Фамилия: {value['last_name']}\n"
                                            f"Имя: {value['first_name']}\n"
                                            f"Профиль: {url + str(value['id'])}\n", photos)
        if start_function_adding_profile:
            adding_profile = VkBot.add_profile_in_list(vk_bot_class_obj, user_id, value['id'])
            list_name.clear()
            return adding_profile
        list_name.clear()