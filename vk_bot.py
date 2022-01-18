import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randrange
from db_orm import session, BanList, FavoriteList


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
        vk_bot_class_obj.write_msg(user_id, f"Понравился Вам человек? Да\Нет.\n")

        for event in vk_bot_class_obj.longpoll_listen():
            if event.type == VkEventType.MESSAGE_NEW:

                if event.to_me:
                    request = event.text

                    if request == 'Да':
                        favorite = FavoriteList(id=profile_id)
                        session.add(favorite)
                        break

                    elif request == 'Нет':
                        ban = BanList(id=profile_id)
                        session.add(ban)
                        break