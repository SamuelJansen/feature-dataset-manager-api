from FlaskHelper import Controller, ControllerMethod
import Role
import UserDto, HttpStatus

@Controller(url = '/users/logout')
class LogoutController:

    @ControllerMethod(url='/<key>', roleRequired=[Role.USER])
    def post(self, key=None):
        self.service.authentication.logout(key)
        return {}, HttpStatus.NO_CONTENT
