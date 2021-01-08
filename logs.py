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
