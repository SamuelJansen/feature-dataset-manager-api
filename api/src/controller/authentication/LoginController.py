from python_framework import Controller, ControllerMethod, HttpStatus

from dto.UserDto import *

@Controller(url = '/authentication/login', tag='Login', description='Login controller')
class LoginController:

    @ControllerMethod(url='/<string:key>',
        requestClass=LoginRequestDto,
        responseClass=LoginResponseDto)
    def post(self, dto, key=None):
        return self.service.authentication.login(dto, key), HttpStatus.CREATED
