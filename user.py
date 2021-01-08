import database as db

class User:
    numOfUsers = 1

    def getProfile(self, id):
        for i in db.users:
            if i["contacts"]["vk"] == id:
                return i

    def createProfile(self, vk_id):
        id = self.numOfUsers
        db.users.append({
            "name": "",
            "password": "",
            "id": id,
            "contacts": {
                "vk": vk_id,
                "telegram": 0,
                "discord": 0
            },
            "orders": [],
            "role": "простой пользователь",
            "act": "none"
        })
        self.numOfUsers += 1

    def editProfile(self, id, edit, value):
        self.getProfile(id)[edit] = value

    def inDb(self, id):
        x = self.getProfile(id)
        if x["name"] != "":
            return True
        else:
            return False

if __name__ == "__main__":
    x = User()
    print(x.numOfUsers)
    x.createProfile(1647674)
    print(x.numOfUsers)
    print(db.users)
    x.editProfile(1647674, "name", "Voiderss")
    print(db.users)
