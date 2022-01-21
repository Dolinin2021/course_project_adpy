import vk_api
from operator import itemgetter


class VkUser():
    """ Класс для работы с аккаунтом Вконтакте.

    :param login: логин ВКонтакте (лучше использовать номер телефона для
        автоматического обхода проверки безопасности)
    :type login: str

    :param token: access_token
    :type token: str

    :param _sex: пол
    :type _sex: int

    :param _status: семейное положение
    :type _status: int

    :param _country_id:  идентификатор страны
    :type _country_id: int

    :param _hometown:  название города строкой
    :type _hometown: str

    :param _age_from:  возраст, от
    :type _age_from: int

    :param _age_do:  возраст, до
    :type _age_do: int

    :param _user_ids:  перечисленные через запятую идентификаторы
            пользователей или их короткие имена (screen_name)
    :type _user_ids: str

    :except: vk_api.AuthError: ошибка авторизации

    """

    def __init__(self, login, token):
        self.login = login
        self.token = token
        self._sex = None
        self._status = None
        self._country_id = None
        self._hometown = None
        self._age_from = None
        self._age_do = None
        self._user_ids = None

        vk_session = vk_api.VkApi(login=self.login, token=self.token)
        try:
            vk_session.auth(token_only=True)
        except vk_api.AuthError as error_msg:
            print(error_msg)
            return
        self.vk = vk_session.get_api()

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

    @property
    def country_id(self):
        return self._country_id

    @country_id.setter
    def country_id(self, value):
        self._country_id = value

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
    def user_ids(self):
        return self._user_ids

    @user_ids.setter
    def user_ids(self, value):
        self._user_ids = value

    def get_albums(self, owner_id):
        """" Вернуть список фотоальбомов пользователя или сообщества.

        :param owner_id: идентификатор пользователя или сообщества,
                    которому принадлежат альбомы.
        :type owner_id: int

        :return albums_list: список фотоальбомов
        :type albums_list: list

        :exception vk_api.exceptions.ApiError: 30 - This profile is private

        Ссылка на официальную документацию: https://vk.com/dev/photos.getAlbums

        """
        albums_list = []
        response = self.vk.photos.getAlbums(owner_id=owner_id)
        for value in response['items']:
            album_dict = {
                'title': value['title'],
                'user_id': value['owner_id'],
                'id': value['id'],
                'size': value['size'],
                'description': value['description']
            }
            albums_list.append(album_dict)
        return albums_list

    def photos_get(self, owner_id, album_id, rev=0, extended=1,  count=1000):
        """" Вернуть список фотографий в альбоме.

        :param owner_id: идентификатор владельца альбома
        :type owner_id: int

        :param album_id: индентификатор альбома.

        Для служебных альбомов используются следующие идентификаторы:
        wall — фотографии со стены;
        profile — фотографии профиля;
        saved — сохраненные фотографии.
        Возвращается только с ключом доступа пользователя в формате строки.

        :type album_id: str

        :param rev: порядок сортировки фотографий.
                1 — антихронологический;
                0 — хронологический.
                По умолчнию равно 0.
        :type rev: int

        :param extended: возвращает дополнительные поля. По умолчнию равно 1.
                    Если был задан параметр extended=1, возвращаются дополнительные поля.
                    Если этот параметр равен нулю, то дополнительные поля не будут выведены.
        :type extended: int

        :param count: количество записей, которое будет получено.
                По умолчнию равно 1000, максимальное значение 1000.
        :type count: int

        :return sorted_list: список фотографий
        :type sorted_list: list

        :exception vk_api.exceptions.ApiError: 30 - This profile is private

        Ссылка на официальную документацию: https://vk.com/dev/photos.get

        """

        photos_list = []
        response = self.vk.photos.get(owner_id=owner_id, album_id=album_id, rev=rev,  extended=extended, count=count)
        for value in response['items']:
            photos_dict = {
                'photo_id': f"{value['id']}",
                'comments_count': f"{value['comments']['count']}",
                'likes_count': f"{value['likes']['count']}",
                'url': value['sizes'][-1]['url']
            }
            photos_list.append(photos_dict)
        sorted_list = sorted(photos_list, key=itemgetter('comments_count', 'likes_count'), reverse=True)
        return sorted_list[:3]

    def users_search(self, age_from=age_from, age_do=age_do, sex=sex, country_id=country_id,
                     hometown=hometown, status=status, count=1000):
        """ Вернуть список пользователей в соответствии с заданными критериями поиска.

        :param age_from:  возраст, от
        :type age_from: int

        :param age_do:  возраст, до
        :type age_do: int

        :param sex: пол
        :type sex: int

        :param country_id:  идентификатор страны
        :type country_id: int

        :param hometown:  название города строкой
        :type hometown: str

        :param status: семейное положение
        :type status: int

        :param  count: количество возвращаемых пользователей.
                По умолчанию равно 1000, максимальное значение 1000.
        :type count: int

        :return: response: результат запроса
        :type: response: dict

        Ссылка на официальную документацию: https://vk.com/dev/users.search

        """

        response = self.vk.users.search(age_from=age_from, age_do=age_do,
                                        sex=sex, country=country_id, hometown=hometown, status=status,
                                        count=count)
        return response

    def users_get(self, user_ids=user_ids):
        """ Вернуть расширенную информацию о пользователях.

        :param user_ids:  перечисленные через запятую идентификаторы
            пользователей или их короткие имена (screen_name).
            Список слов, разделенных через запятую,
            количество элементов должно составлять не более 1000.
        :type user_ids: str

        :return: user_list: список с информацией о пользователе
        :type: user_list: list

        :exception: 3610 - User is deactivated

        Ссылка на официальную документацию: https://vk.com/dev/users.get

        """
        user_list = []
        response = self.vk.users.get(user_ids=user_ids)
        for value in response:
            user_dict = {
                'id': value['id'],
                'last_name': value['last_name'],
                'first_name': value['first_name'],
                'is_closed': value['is_closed'],
                'can_access_closed': value['can_access_closed']
            }
            user_list.append(user_dict)
        return user_list

    @staticmethod
    def get_countries(login, token, need_all=1, count=1000):
        """ Вернуть список стран.

        :param login: логин ВКонтакте (лучше использовать номер телефона для
        автоматического обхода проверки безопасности)
        :type login: str

        :param token: access_token
        :type token: str

        :param need_all: вернуть список всех стран.
                    Флаг, может принимать значения 1 или 0, по умолчанию равен 1.
        :type need_all: int

        :param count: количество стран, которое необходимо вернуть.
                По умолчанию равно 1000, максимальное значение 1000.

        :return: country_list: список стран
        :type: country_list: list

        :except: vk_api.AuthError: ошибка авторизации

        Ссылка на официальную документацию: https://vk.com/dev/database.getCountries

        """

        country_list = []

        vk_session = vk_api.VkApi(login=login, token=token)
        try:
            vk_session.auth(token_only=True)
        except vk_api.AuthError as error_msg:
            print(error_msg)
        vk = vk_session.get_api()

        response = vk.database.getCountries(need_all=need_all, count=count)
        for value in response['items']:
            country_dict = {value['title']: value['id']}
            country_list.append(country_dict)

        return country_list