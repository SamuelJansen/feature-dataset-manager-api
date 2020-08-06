from FlaskManager import Controller, ControllerMethod
from Role import *
import UserDto, HttpStatus

@Controller(url = '/authentication/logout')
class LogoutController:

    @ControllerMethod(url='/<string:key>', roleRequired=[USER, ADMIN])
    def post(self, key=None):
        self.service.authentication.logout(key)
        return {}, HttpStatus.NO_CONTENT
