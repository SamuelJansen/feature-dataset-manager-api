from python_framework import Controller, ControllerMethod, HttpStatus
import UserDto

@Controller(url = '/authentication/login', tag='Login', description='Login controller')
class LoginController:

    @ControllerMethod(url='/<string:key>',
        requestClass=UserDto.LoginRequestDto,
        responseClass=UserDto.LoginResponseDto)
    def post(self, dto, key=None):
        return self.service.authentication.login(dto, key), HttpStatus.CREATED
