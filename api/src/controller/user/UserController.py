from python_framework import Controller, ControllerMethod, HttpStatus
from Role import *
import UserDto

@Controller(url = '/users', tag='User', description='Single User controller')
class UserController:

    @ControllerMethod(url='/<string:key>',
        requestClass=UserDto.UserRequestDto,
        responseClass=UserDto.UserResponseDto)
    def post(self, dto, key):
        return self.service.user.create(dto, key), HttpStatus.CREATED

    @ControllerMethod(url='/<string:key>',
        responseClass=UserDto.UserResponseDto,
        roleRequired=[USER, ADMIN])
    def get(self, key):
        return self.service.user.queryByKey(key), HttpStatus.OK

    @ControllerMethod(url='/<string:key>',
        requestClass=UserDto.UserRequestDto,
        responseClass=UserDto.UserResponseDto,
        roleRequired=[USER, ADMIN])
    def put(self, dto, key):
        return self.service.user.update(dto, key), HttpStatus.ACCEPTED

    @ControllerMethod(url='/<string:key>', roleRequired=[ADMIN])
    def delete(self, key):
        self.service.user.delete(key), HttpStatus.NO_CONTENT
        return {}, HttpStatus.NO_CONTENT

@Controller(url = '/users/batch', tag='User', description='Multiple User controller')
class UserBatchController:

    @ControllerMethod(
        responseClass=[[UserDto.UserResponseDto]],
        roleRequired=[ADMIN])
    def get(self):
        return self.service.user.queryAll(), HttpStatus.OK
