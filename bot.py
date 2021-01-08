import vk_api, vk
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from config import info
from user import User
import logs

class Bot:
    def __init__(self, i):
        self.reg = VkKeyboard(one_time=True)
        self.reg.add_button('Зарегистрироваться', color=VkKeyboardColor.POSITIVE)

        self.main = VkKeyboard(one_time=True)
        self.main.add_button("Профиль")

        self.token = i["token"]
        self.group_id = i["group_id"]
        self.key = i["key"]
        self.server = i["server"]
        self.ts = i["ts"]

        self.vk_session = vk_api.VkApi(token=self.token)
        self.longpoll = VkLongPoll(self.vk_session)
        self.vk = self.vk_session.get_api()

    def start_msg(self, peer):
        x = User()
        if x.getProfile(peer) == None:
            keyboard = self.reg.get_keyboard()
        else:
            keyboard = self.main.get_keyboard()
        self.vk.messages.send(
            user_id = peer,
            random_id = get_random_id(),
            keyboard = keyboard,
            message = "Привет, я бот Daruna, чем могу помочь?"
            )

    def send_msg(self, text, peer, key):
        if key == "main":
            key = self.main.get_keyboard()
        else:
            key = None
        self.vk.messages.send(
            user_id = peer,
            random_id = get_random_id(),
            message = text,
            keyboard = key
            )

    def start(self):
        user = User()
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                text = event.text.lower()
                author = event.user_id
                if text.lower() == "начать":
                    self.start_msg(author)
                    user.createProfile(author)
                    continue

                act = user.getProfile(author)["act"]

                if text.lower() == "зарегистрироваться":
                    if user.inDb(author):
                        self.send_msg("Вы уже зарегистрированны", author, "main")
                    else:
                        self.send_msg("Введите имя для вашего аккаунта", author, None)
                        user.getProfile(author)["act"] = "registr(name)"
                else:
                    if act == "registr(name)":
                        user.editProfile(author, "name", text)
                        self.send_msg("Введите пароль для вашего аккаунта", author, None)
                        user.getProfile(author)["act"] = "registr(password)"
                    elif act == "registr(password)":
                        user.editProfile(author, "password", text)
                        self.send_msg("Регистрация завершена", author, "main")
                        logs.newUser(author)
                        user.getProfile(author)["act"] = "main"
                    else:
                        break

if __name__ == "__main__":
    x = Bot(info)
    x.start()
