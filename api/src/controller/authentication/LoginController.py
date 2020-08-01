from FlaskHelper import Controller, ControllerMethod
import UserDto, HttpStatus

@Controller(url = '/users/login')
class LoginController:

    @ControllerMethod(url='/<key>', requestClass=UserDto.UserRequestDto)
    def post(self, dto, key=None):
        return self.service.authentication.login(dto, key), HttpStatus.CREATED
