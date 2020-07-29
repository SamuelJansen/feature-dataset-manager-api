from FlaskHelper import Converter, ConverterMethod
import Feature, FeatureDto

@Converter()
class FeatureConverter:

    @ConverterMethod(requestClass=Feature.Feature, responseClass=FeatureDto.FeatureResponseDto)
    def fromModelToResponseDto(self, model, dto) :
        return dto

    @ConverterMethod(requestClass=[[Feature.Feature]])
    def fromModelListToResponseDtoList(self,modelList):
        responseDtoList = []
        for model in modelList :
            responseDtoList.append(self.fromModelToResponseDto(model))
        return responseDtoList
