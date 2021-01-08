from user import User

def newUser(id):
    x = User()
    profile = x.getProfile(id)
    print("\n============================")
    print("новый пользователь")
    print(f"id - {profile['id']}")
    print(f"vk id - {profile['contacts']['vk']}")
    print(f"имя - {profile['name']}")
    print(f"пароль - {profile['password']}")
    print("============================")

def cheangeLogin(id, old_login, new_login):
    print("\n============================")
    print(f"пользователь {id} сменил логин")
    print(f"старый логин - {old_login}")
    print(f"новый логин - {new_login}")
    print("============================")

def cheangePassword(id, old_pass, new_login):
    print("\n============================")
    print(f"пользователь {id} сменил пароль")
    print(f"старый пароль - {old_pass}")
    print(f"новый пароль - {new_login}")
    print("============================")
