import database as db

class User:
    numOfUsers = 1

    def getProfile(self, id):
        for i in db.data["users"]:
            if i["contacts"]["vk"] == id:
                return i

    def createProfile(self, vk_id):
        id = self.numOfUsers
        db.data["users"].append({
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
            "moder": False,
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
