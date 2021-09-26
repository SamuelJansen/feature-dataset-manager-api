from python_framework import Controller, ControllerMethod, HttpStatus
from Role import *

from dto.UserDto import *

@Controller(url = '/users', tag='User', description='Single User controller')
class UserController:

    @ControllerMethod(url='/<string:key>',
        requestClass=UserRequestDto,
        responseClass=UserResponseDto)
    def post(self, dto, key):
        return self.service.user.create(dto, key), HttpStatus.CREATED

    @ControllerMethod(url='/<string:key>',
        responseClass=UserResponseDto,
        roleRequired=[USER, ADMIN, API])
    def get(self, key):
        return self.service.user.queryByKey(key), HttpStatus.OK

    @ControllerMethod(url='/<string:key>',
        requestClass=UserRequestDto,
        responseClass=UserResponseDto,
        roleRequired=[USER, ADMIN, API])
    def put(self, dto, key):
        return self.service.user.update(dto, key), HttpStatus.ACCEPTED

    @ControllerMethod(url='/<string:key>',
        roleRequired=[ADMIN, API])
    def delete(self, key):
        self.service.user.delete(key), HttpStatus.NO_CONTENT
        return {}, HttpStatus.NO_CONTENT

@Controller(url = '/users/batch', tag='User', description='Multiple User controller')
class UserBatchController:

    @ControllerMethod(
        responseClass=[[UserResponseDto]],
        roleRequired=[ADMIN, API])
    def get(self):
        return self.service.user.queryAll(), HttpStatus.OK
