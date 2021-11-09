from python_framework import Converter, ConverterMethod

from Feature import Feature

from dto.FeatureDto import FeatureResponseDto

@Converter()
class FeatureConverter:

    @ConverterMethod(requestClass=Feature, responseClass=FeatureResponseDto)
    def fromModelToResponseDto(self, model, dto):
        return dto

    @ConverterMethod(requestClass=[[Feature]])
    def fromModelListToResponseDtoList(self,modelList):
        responseDtoList = []
        for model in modelList :
            responseDtoList.append(self.fromModelToResponseDto(model))
        return responseDtoList
