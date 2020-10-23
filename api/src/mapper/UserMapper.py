from python_framework import Mapper, MapperMethod
import User, UserDto
import Role

@Mapper()
class UserMapper:

    @MapperMethod(requestClass=[UserDto.UserRequestDto, str], responseClass=User.User)
    def fromPostRequestDtoToModel(self, dto, key, model) :
        model.key = key
        model.role = Role.USER
        return model

    @MapperMethod(requestClass=[UserDto.UserRequestDto, User.User])
    def overrideModelValues(self, dto, model):
        model.email = dto.email
