from python_framework import Converter, ConverterMethod

from User import User
from dto.UserDto import LoginResponseDto, UserResponseDto

@Converter()
class UserConverter:

    @ConverterMethod(requestClass=User, responseClass=UserResponseDto)
    def fromModelToResponseDto(self, model, dto) :
        return dto

    @ConverterMethod(requestClass=[[User]])
    def fromModelListToResponseDtoList(self,modelList):
        responseDtoList = []
        for model in modelList :
            responseDtoList.append(self.fromModelToResponseDto(model))
        return responseDtoList

    @ConverterMethod(requestClass=[User, str], responseClass=LoginResponseDto)
    def fromModelToLoginResponseDto(self, model, accessToken, dto) :
        dto.accessToken = accessToken
        return dto
