from python_framework import Converter, ConverterMethod
import FeatureData, FeatureDataDto

@Converter()
class FeatureDataConverter:

    @ConverterMethod(requestClass=FeatureData.FeatureData, responseClass=FeatureDataDto.FeatureDataResponseDto)
    def fromModelToResponseDto(self, model, dto) :
        dto.featureKey = model.feature.key
        dto.sampleKey = model.sample.key
        return dto

    @ConverterMethod(requestClass=[[FeatureData.FeatureData]])
    def fromModelListToResponseDtoList(self, modelList):
        responseDtoList = []
        for model in modelList :
            responseDtoList.append(self.fromModelToResponseDto(model))
        return responseDtoList
