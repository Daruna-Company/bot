import vk_api, vk
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from config import info
from user import User
import database as db
import logs

class Bot:
    def __init__(self, i):
        self.reg = VkKeyboard(one_time=True)
        self.reg.add_button('Зарегистрироваться', color=VkKeyboardColor.POSITIVE)

        self.main = VkKeyboard(one_time=True)
        self.main.add_button("Профиль")

        self.profile = VkKeyboard(one_time=True)
        self.profile.add_button("Изменить логин")
        self.profile.add_button("Изменить пароль")
        self.profile.add_line()
        self.profile.add_button("Назад", color=VkKeyboardColor.NEGATIVE)

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
        elif key == "profile":
            key = self.profile.get_keyboard()
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
                ltext = event.text
                text = event.text.lower()
                author = event.user_id
                if text.lower() == "начать":
                    self.start_msg(author)
                    user.createProfile(author)
                    continue

                act = user.getProfile(author)["act"]

                if text == "зарегистрироваться":
                    if user.inDb(author):
                        self.send_msg("Вы уже зарегистрированны", author, "main")
                    else:
                        self.send_msg("Введите логин для вашего аккаунта", author, None)
                        user.getProfile(author)["act"] = "registr(login)"
                else:
                    if act == "registr(login)":
                        if ltext in db.data["logins"]:
                            self.send_msg("Введённый вами логин уже используется, попробуйте другой", author, None)
                        elif len(ltext) < 3:
                            self.send_msg("Введённый вами логин слишком короткий(необходимо хотя бы 3 символов),\
 попробуйте другой", author, None)
                        elif len(ltext) >= 30:
                            self.send_msg("Введённый вами логин слишком длинный(необходимо не больше 30 символов),\
 попробуйте другой", author, None)
                        else:
                            user.editProfile(author, "name", ltext)
                            db.data["logins"].append(ltext)
                            self.send_msg("Введите пароль для вашего аккаунта", author, None)
                            user.getProfile(author)["act"] = "registr(password)"
                    elif act == "registr(password)":
                        test = User.cheakPassword(ltext)
                        if test == -1:
                            self.send_msg("Введённый вами пароль слишком маленький(минимум 7 символов), попробуйте другой", author, None)
                        elif test == -2:
                            self.send_msg("Введённый вами пароль не содержит заглавные буквы, попробуйте другой", author, None)
                        elif test == -3:
                            self.send_msg("Введённый вами пароль не содержит строчные буквы, попробуйте другой", author, None)
                        elif test == -4:
                            self.send_msg("Введённый вами пароль не содержит цифры, попробуйте другой", author, None)
                        elif test == -5:
                            self.send_msg("Введённый вами пароль содержит пробелы, попробуйте другой", author, None)
                        elif test == 1:
                            user.editProfile(author, "password", ltext)
                            self.send_msg("Регистрация завершена", author, "main")
                            logs.newUser(author)
                            user.getProfile(author)["act"] = "main"
                    elif act == "cheangeLogin":
                        if ltext == user.getProfile(author)["name"]:
                            self.send_msg("Введенный вами логин совпадает со старым, придумаете другой", author, None)
                        else:
                            old_login = user.getProfile(author)["name"]
                            self.send_msg("Логин изменён", author, "profile")
                            db.data["logins"].remove(old_login)
                            user.getProfile(author)["name"] = ltext
                            logs.cheangeLogin(user.getProfile(author)["id"], old_login, ltext)
                            user.getProfile(author)["act"] = "profile"
                    elif act == "cheangePassword":
                        if ltext == user.getProfile(author)["password"]:
                            self.send_msg("Введенный вами пароль совпадает со старым, придумаете другой", author, None)
                        else:
                            old_pass = user.getProfile(author)["password"]
                            self.send_msg("Пароль изменён", author, "profile")
                            user.getProfile(author)["password"] = ltext
                            logs.cheangeLogin(user.getProfile(author)["id"], old_pass, ltext)
                            user.getProfile(author)["act"] = "profile"
                    elif act == "getOldPassword":
                        if ltext != user.getProfile(author)["password"]:
                            self.send_msg("Введенный вами пароль не совпадает с нынешним, попробуйте ещё раз", author, None)
                        else:
                            self.send_msg("Введите новый пароль", author, None)
                            user.getProfile(author)["act"] = "cheangePassword"
                    elif text == "профиль" and act == "main":
                        people = user.getProfile(author)
                        self.send_msg(f"Ваш аккаунт:\nid - {people['id']}\nлогин - {people['name']}\
\nроль - {people['role']}", author, "profile")
                        user.getProfile(author)["act"] = "profile"
                    elif text == "изменить логин" and act == "profile":
                        self.send_msg("Введите новый логин", author, None)
                        user.getProfile(author)["act"] = "cheangeLogin"
                    elif text == "изменить пароль" and act == "profile":
                        self.send_msg("Чтобы установить новый пароль введите нынешний", author, None)
                        user.getProfile(author)["act"] = "getOldPassword"
                    elif text == "назад" and act == "profile":
                        self.send_msg("Чем могу помочь?", author, "main")
                        user.getProfile(author)["act"] = "main"
                    else:
                        break

if __name__ == "__main__":
    x = Bot(info)
    x.start()
