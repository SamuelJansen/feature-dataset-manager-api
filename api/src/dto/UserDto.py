class UserRequestDto:
    def __init__(self,
        username = None,
        password = None,
        email = None
    ):
        self.username = username
        self.password = password
        self.email = email

class UserResponseDto:
    def __init__(self,
        key = None,
        username = None,
        email = None
    ):
        self.key = key
        self.username = username
        self.email = email

class LoginRequestDto:
    def __init__(self,
        password = None,
        email = None
    ):
        self.password = password
        self.email = email

class LoginResponseDto:
    def __init__(self,
        accessToken = None
    ):
        self.accessToken = accessToken
