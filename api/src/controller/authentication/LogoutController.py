from python_framework import Controller, ControllerMethod, HttpStatus
from Role import *

from dto.UserDto import *

@Controller(url = '/authentication/logout', tag='Logout', description='Logout controller')
class LogoutController:

    @ControllerMethod(url='/<string:key>',
        roleRequired=[USER, ADMIN, API])
    def post(self, key=None):
        self.service.authentication.logout(key)
        return {}, HttpStatus.NO_CONTENT
