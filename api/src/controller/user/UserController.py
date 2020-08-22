from FlaskManager import Controller, ControllerMethod
from Role import *
import UserDto, HttpStatus

@Controller(url = '/users', tag='User', description='Single User controller')
class UserController:

    @ControllerMethod(url='/<string:key>', requestClass=UserDto.UserRequestDto)
    def post(self, dto, key):
        return self.service.user.create(dto, key), HttpStatus.CREATED

    @ControllerMethod(url='/<string:key>', roleRequired=[USER, ADMIN])
    def get(self, key):
        return self.service.user.queryByKey(key), HttpStatus.OK

    @ControllerMethod(url='/<string:key>', requestClass=UserDto.UserRequestDto, roleRequired=[USER, ADMIN])
    def put(self, dto, key):
        return self.service.user.update(dto, key), HttpStatus.ACCEPTED

    @ControllerMethod(url='/<string:key>', roleRequired=[ADMIN])
    def delete(self, key):
        self.service.user.delete(key), HttpStatus.NO_CONTENT
        return {}, HttpStatus.NO_CONTENT

@Controller(url = '/users', tag='User', description='Multiple User controller')
class UserBatchController:

    @ControllerMethod(url='/', roleRequired=[ADMIN])
    def get(self):
        return self.service.user.queryAll(), HttpStatus.OK
