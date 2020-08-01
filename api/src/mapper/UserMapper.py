from FlaskManager import Mapper, MapperMethod
import User, UserDto

@Mapper()
class UserMapper:

    @MapperMethod(requestClass=[UserDto.UserRequestDto, str], responseClass=User.User)
    def fromPostRequestDtoToModel(self, dto, key, model) :
        model.key = key
        return model

    @MapperMethod(requestClass=[UserDto.UserRequestDto, User.User])
    def overrideModelValues(self, dto, model):
        model.email = dto.email
