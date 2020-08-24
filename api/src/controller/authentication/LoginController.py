from FlaskManager import Controller, ControllerMethod
import UserDto, HttpStatus

@Controller(url = '/authentication/login', tag='Login', description='Login controller')
class LoginController:

    @ControllerMethod(url='/<string:key>',
        requestClass=UserDto.LoginRequestDto,
        responseClass=UserDto.LoginResponseDto)
    def post(self, dto, key=None):
        print(key)
        return self.service.authentication.login(dto, key), HttpStatus.CREATED
