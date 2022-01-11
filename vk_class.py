import vk_api
from pprint import pprint
from operator import itemgetter


class VkUser():

    def __init__(self, login, token):
        self.login = login
        self.token = token
        self._sex = None
        self._status = None
        self._relation = None
        self._hometown = None
        self._age_from = None
        self._age_do = None
        self._count = None
        # self._country_id = None
        self._user_ids = None
        vk_session = vk_api.VkApi(login=self.login, token=self.token)
        try:
            vk_session.auth(token_only=True)
        except vk_api.AuthError as error_msg:
            print(error_msg)
            return
        self.vk = vk_session.get_api()

    # @property
    # def text(self):
    #     return self._text
    #
    # @text.setter
    # def text(self, value):
    #     self._text = value

    @property
    def age_from(self):
        return self._age_from

    @age_from.setter
    def age_from(self, value):
        self._age_from = value

    @property
    def age_do(self):
        return self._age_do

    @age_do.setter
    def age_do(self, value):
        self._age_do = value

    @property
    def sex(self):
        return self._sex

    @sex.setter
    def sex(self, value):
        self._sex = value

    # @property
    # def country(self):
    #     return self._country_id
    #
    # @country.setter
    # def country(self, value):
    #     self._country_id = value

    @property
    def hometown(self):
        return self._hometown

    @hometown.setter
    def hometown(self, value):
        self._hometown = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, value):
        self._count = value

    @property
    def user_ids(self):
        return self._user_ids

    @user_ids.setter
    def user_ids(self, value):
        self._user_ids = value

    def photos_get(self, owner_id, album_id='profile', rev=0, extended=1,  count=10):

        photos_list = []

        response = self.vk.photos.get(owner_id=owner_id, album_id=album_id, rev=rev,  extended=extended, count=count)

        for value in response['items']:

            photos_dict = {
                'comments_count': f"{value['comments']['count']}",
                'likes_count': f"{value['likes']['count']}",
                'url': value['sizes'][-1]['url']
            }

            photos_list.append(photos_dict)

        sorted_list = sorted(photos_list, key=itemgetter('comments_count', 'likes_count'), reverse=True)

        return sorted_list[:3]

    def users_search(self, age_from=age_from, age_do=age_do, sex=sex, hometown=hometown, status=status, count=count):

        response = self.vk.users.search(age_from=age_from, age_do=age_do,
                                        sex=sex, hometown=hometown, status=status,
                                        count=count)

        return response['items']

    def users_get(self, user_ids=user_ids):

        res_user_list = []

        response = self.vk.users.get(user_ids=user_ids, fields='sex,country,city,relation')

        # pprint(response)

        try:
            for value in response:
                user_dict = {
                    'id': value['id'],
                    'last_name': value['last_name'],
                    'first_name': value['first_name'],
                    'is_closed': value['is_closed'],
                    'can_access_closed': value['can_access_closed'],
                    'sex': value['sex'],
                    'country': value['country']['title'],
                    'city': value['city']['title'],
                    'relation': value['relation']
                }
                res_user_list.append(user_dict)

        except KeyError:
            for value in response:
                user_dict = {
                    'id': value['id'],
                    'last_name': value['last_name'],
                    'first_name': value['first_name'],
                    'is_closed': value['is_closed'],
                    'can_access_closed': value['can_access_closed'],
                }
                res_user_list.append(user_dict)

        return res_user_list