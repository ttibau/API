from modules.login.steam import Steam


class Login:
    def __init__(self, obj):
        self.steam = Steam(obj=obj)
