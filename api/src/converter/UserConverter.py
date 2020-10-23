from python_framework import Converter, ConverterMethod
import User, UserDto

@Converter()
class UserConverter:

    @ConverterMethod(requestClass=User.User, responseClass=UserDto.UserResponseDto)
    def fromModelToResponseDto(self, model, dto) :
        return dto

    @ConverterMethod(requestClass=[[User.User]])
    def fromModelListToResponseDtoList(self,modelList):
        responseDtoList = []
        for model in modelList :
            responseDtoList.append(self.fromModelToResponseDto(model))
        return responseDtoList

    @ConverterMethod(requestClass=[User.User, str], responseClass=UserDto.LoginResponseDto)
    def fromModelToLoginResponseDto(self, model, accessToken, dto) :
        dto.accessToken = accessToken
        return dto
