from python_framework import Converter, ConverterMethod

from FeatureData import FeatureData

from dto.FeatureDataDto import FeatureDataResponseDto

@Converter()
class FeatureDataConverter:

    @ConverterMethod(requestClass=FeatureData, responseClass=FeatureDataResponseDto)
    def fromModelToResponseDto(self, model, dto):
        dto.featureKey = feature.key
        dto.sampleKey = sample.key
        return dto

    @ConverterMethod(requestClass=[[FeatureData]])
    def fromModelListToResponseDtoList(self, modelList):
        responseDtoList = []
        for model in modelList :
            responseDtoList.append(self.fromModelToResponseDto(model))
        return responseDtoList
