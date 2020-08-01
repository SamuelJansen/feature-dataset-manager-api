from FlaskHelper import Service, ServiceMethod
import Security, Role, HttpStatus
import User, UserDto

@Service()
class AuthenticationService:

    @ServiceMethod(requestClass=[UserDto.LoginRequestDto, str])
    def login(self, dto, key):
        self.validator.user.loginRequestDto(dto, key)
        model = self.service.user.findByKey(key)
        self.validator.user.password(dto, model)
        accessToken = Security.createAccessToken(model)
        return {'accessToken' : accessToken}

    @ServiceMethod(requestClass=str)
    def logout(self, key):
        self.validator.common.pathVariableNotNull(key, 'key')
        model = self.service.user.findByKey(key)
        self.validator.user.loggedUser(model)
        Security.addUserToBlackList()
