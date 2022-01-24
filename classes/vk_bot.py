import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randrange
from classes.db_orm import session, FavoriteList, BanList, favorite_list, ban_list


class VkBot:
    """ Класс для работы с ботом Вконтакте.

    :param login: логин ВКонтакте (лучше использовать номер телефона для
        автоматического обхода проверки безопасности)
    :type login: str

    :param token: access_token
    :type token: str

    """

    def __init__(self, login, token):
        self.login = login
        self.token = token
        self.vk_session = vk_api.VkApi(login=self.login, token=self.token)

    def longpoll_listen(self):
        """"Вернуть метод прослушивания longpoll-сервера."""

        longpoll = VkLongPoll(self.vk_session, group_id=209853199)
        return longpoll.listen()

    def write_msg(self, user_id, message, photo=None):
        """ Вызвать метод VK API messages.send.

        :param user_id: id пользователя
        :type user_id: int

        :param message: текст сообщения
        :type message: str

        :param photo: фотографии, которые нужно отправить в чат пользователю
        :type photo: str

        """

        self.vk_session.method('messages.send',
                               {'user_id': user_id, 'message': message, 'attachment': photo, 'random_id': randrange(10 ** 7)})

    def add_profile_in_list(self, user_id, profile_id):
        """ Добавь пользователя в список.

        :param user_id: id пользователя
        :type user_id: int

        :param profile_id: id запрашиваемого профиля
        :type profile_id: int

        :return break_out_flag: переменная-флаг, которая показывает программе,
                        когда выходить из внешнего цикла. Возвращает либо True, либо False.
        :type break_out_flag: bool

        """

        self.write_msg(user_id, "Понравился ли Вам человек? \n")
        self.write_msg(user_id, "Введите команду 'Да', чтобы добавить в 'Избранное'. \n")
        self.write_msg(user_id, "Введите команду 'Нет', чтобы добавить в чёрный список. \n")
        self.write_msg(user_id, "Введите команду 'Продолжить', чтобы пропустить текущего пользователя. \n")
        self.write_msg(user_id, "Введите команду 'Стоп', чтобы остановить поиск. \n")
        self.write_msg(user_id, "Если текущий поиск окончен, введите команду 'Запуск', чтобы начать новый поиск.")

        for event in self.longpoll_listen():
            if event.type == VkEventType.MESSAGE_NEW:

                if event.to_me:
                    request = event.text

                    if request == "Да":
                        favorite = FavoriteList(id=profile_id)
                        favorite_list.append(profile_id)
                        session.add(favorite)
                        session.commit()
                        break

                    elif request == "Нет":
                        ban = BanList(id=profile_id)
                        ban_list.append(profile_id)
                        session.add(ban)
                        session.commit()
                        break

                    elif request == "Продолжить":
                        break

                    elif request == "Стоп":
                        self.write_msg(user_id, "Поиск остановлен. \n"
                                                "Чтобы начать новый поиск, введите команду 'Запуск'. \n"
                                                "Чтобы увидеть понравившихся пользователей, введите команду 'Избранное'. \n"
                                                "Чтобы выйти из программы, введите команду 'Выход'.")
                        break_out_flag = True
                        return break_out_flag

                    else:
                        self.write_msg(user_id, "Неверная команда. Попробуйте ещё раз.")

    def query_result(self, value, user_id, url, list_name, start=True):
        """ Выведи в чат результат выполнения запроса users.get.

        :param value: информация о пользователе в результате выполнения запроса
        :type value: dict

        :param user_id: id пользователя
        :type user_id: int

        :param url: адрес пользователя
        :type url: str

        :param list_name: список фотографий
        :type list_name: list

        :param start: вывод окна по добавлению пользователя в список (запуск метода add_profile_in_list).
                Возвращает либо True, либо False. По умолчанию равно True.
        :type start: bool

        :return adding_profile: результат выполнения метода add_profile_in_list.
                                Возвращает либо True, либо False.
        :type adding_profile: bool

        """

        photos = ','.join(list_name[:3])
        self.write_msg(user_id, f"Фамилия: {value['last_name']}\n"
                                f"Имя: {value['first_name']}\n"
                                f"Профиль: {url + str(value['id'])}\n", photos)
        if start:
            adding_profile = self.add_profile_in_list(user_id, value['id'])
            list_name.clear()
            return adding_profile
        list_name.clear()