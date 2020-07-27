from FlaskHelper import Converter, ConverterMethod
import Feature, FeatureDto

@Converter()
class FeatureConverter:

    @ConverterMethod(responseClass=FeatureDto.FeatureResponseDto)
    def fromModelToResponseDto(self, model, dto) :
        return dto

    @ConverterMethod()
    def fromModelListToResponseDtoList(self,sampleList):
        responseDtoList = []
        for sample in sampleList :
            responseDtoList.append(self.fromModelToResponseDto(sample))
        return responseDtoList
