from python_framework import Controller, ControllerMethod, HttpStatus
from Role import *
import UserDto

@Controller(url = '/authentication/logout', tag='Logout', description='Logout controller')
class LogoutController:

    @ControllerMethod(url='/<string:key>',
        roleRequired=[USER, ADMIN])
    def post(self, key=None):
        self.service.authentication.logout(key)
        return {}, HttpStatus.NO_CONTENT
