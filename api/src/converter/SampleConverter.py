from python_framework import Converter, ConverterMethod
import Sample, SampleDto, FeatureDataDto, BestFitDto

@Converter()
class SampleConverter:

    @ConverterMethod(requestClass=Sample.Sample, responseClass=SampleDto.SampleResponseDto)
    def fromModelToResponseDto(self, model, dto) :
        dto.featureDataList = []
        for featureData in model.featureDataList :
            dto.featureDataList.append(
                FeatureDataDto.FeatureDataResponseDto(
                    value = featureData.value,
                    iterationCount = featureData.iterationCount,
                    featureKey = featureData.feature.key,
                    sampleKey = featureData.sample.key
                )
            )
        return dto

    @ConverterMethod(requestClass=[[Sample.Sample]])
    def fromModelListToResponseDtoList(self,modelList):
        responseDtoList = []
        for model in modelList :
            responseDtoList.append(self.fromModelToResponseDto(model))
        return responseDtoList

    @ConverterMethod(requestClass=Sample.Sample, responseClass=BestFitDto.BestFitResponseDto)
    def fromModelToBestFitResponseDto(self, model, dto) :
        dto.featureDataList = []
        for featureData in model.featureDataList :
            dto.featureDataList.append(
                FeatureDataDto.FeatureDataResponseDto(
                    value = featureData.value,
                    iterationCount = featureData.iterationCount,
                    featureKey = featureData.feature.key,
                    sampleKey = featureData.sample.key
                )
            )
        return dto

    @ConverterMethod(requestClass=[[Sample.Sample]])
    def fromModelListToBestFitResponseDtoList(self,modelList):
        responseDtoList = []
        for model in modelList :
            responseDtoList.append(self.fromModelToBestFitResponseDto(model))
        return responseDtoList
