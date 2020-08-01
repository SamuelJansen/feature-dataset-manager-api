from FlaskHelper import Controller, ControllerMethod
import Role
import UserDto, HttpStatus

@Controller(url = '/users')
class UserController:

    @ControllerMethod(url='/<key>', requestClass=UserDto.UserRequestDto)
    def post(self, dto, key):
        return self.service.user.create(dto, key), HttpStatus.CREATED

    @ControllerMethod(url='/<key>', roleRequired=[Role.USER])
    def get(self, key):
        return self.service.user.queryByKey(key), HttpStatus.OK

    @ControllerMethod(url='/<key>', requestClass=UserDto.UserRequestDto, roleRequired=[Role.USER])
    def put(self, dto, key):
        return self.service.user.update(dto, key), HttpStatus.ACCEPTED

    @ControllerMethod(url='/<key>', roleRequired=[Role.ADMIN])
    def delete(self, key):
        self.service.user.delete(key), HttpStatus.NO_CONTENT
        return {}, HttpStatus.NO_CONTENT

@Controller(url = '/users')
class UserBatchController:

    @ControllerMethod(url='/', roleRequired=[Role.ADMIN])
    def get(self):
        return self.service.user.queryAll(), HttpStatus.OK
