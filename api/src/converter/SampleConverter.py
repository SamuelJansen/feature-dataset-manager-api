from FlaskHelper import Converter, ConverterMethod
import Sample, SampleDto, FeatureDataDto

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
