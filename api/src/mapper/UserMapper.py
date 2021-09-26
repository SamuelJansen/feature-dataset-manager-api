from python_framework import Mapper, MapperMethod

from User import User
from dto.UserDto import UserRequestDto

import Role

@Mapper()
class UserMapper:

    @MapperMethod(requestClass=[UserRequestDto, str], responseClass=User)
    def fromPostRequestDtoToModel(self, dto, key, model) :
        model.key = key
        model.role = Role.USER
        return model

    @MapperMethod(requestClass=[UserRequestDto, User])
    def overrideModelValues(self, dto, model):
        model.email = dto.email
