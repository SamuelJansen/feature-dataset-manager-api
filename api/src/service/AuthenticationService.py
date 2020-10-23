from python_framework import Service, ServiceMethod, Security
import User, UserDto

@Service()
class AuthenticationService:

    @ServiceMethod(requestClass=[UserDto.LoginRequestDto, str])
    def login(self, dto, key):
        VALID_TOKEN_MINUTES_DURATION = 30
        self.validator.user.loginRequestDto(dto, key)
        model = self.service.user.findByKey(key)
        self.validator.user.password(dto, model)
        accessToken = Security.createAccessToken(model, deltaMinutes=VALID_TOKEN_MINUTES_DURATION)
        return self.converter.user.fromModelToLoginResponseDto(model, accessToken)

    @ServiceMethod(requestClass=str)
    def logout(self, key):
        self.validator.common.pathVariableNotNull(key, 'key')
        model = self.service.user.findByKey(key)
        self.validator.user.loggedUser(model)
        Security.addUserToBlackList()
