from python_framework import Converter, ConverterMethod

from Sample import Sample

from dto.SampleDto import SampleResponseDto
from dto.FeatureDataDto import FeatureDataResponseDto
from dto.BestFitDto import BestFitResponseDto

@Converter()
class SampleConverter:

    @ConverterMethod(requestClass=Sample, responseClass=SampleResponseDto)
    def fromModelToResponseDto(self, model, dto) :
        dto.featureDataList = []
        for featureData in model.featureDataList :
            dto.featureDataList.append(
                FeatureDataResponseDto(
                    value = featureData.value,
                    iterationCount = featureData.iterationCount,
                    featureKey = featureData.feature.key,
                    sampleKey = featureData.sample.key
                )
            )
        return dto

    @ConverterMethod(requestClass=[[Sample]])
    def fromModelListToResponseDtoList(self,modelList):
        responseDtoList = []
        for model in modelList :
            responseDtoList.append(self.fromModelToResponseDto(model))
        return responseDtoList

    @ConverterMethod(requestClass=Sample, responseClass=BestFitResponseDto)
    def fromModelToBestFitResponseDto(self, model, dto) :
        dto.featureDataList = []
        for featureData in model.featureDataList :
            dto.featureDataList.append(
                FeatureDataResponseDto(
                    value = featureData.value,
                    iterationCount = featureData.iterationCount,
                    featureKey = featureData.feature.key,
                    sampleKey = featureData.sample.key
                )
            )
        return dto

    @ConverterMethod(requestClass=[[Sample]])
    def fromModelListToBestFitResponseDtoList(self,modelList):
        responseDtoList = []
        for model in modelList :
            responseDtoList.append(self.fromModelToBestFitResponseDto(model))
        return responseDtoList
