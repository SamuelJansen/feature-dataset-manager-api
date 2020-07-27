from FlaskHelper import Converter, ConverterMethod
import Sample, SampleDto, FeatureDataDto

@Converter()
class SampleConverter:

    @ConverterMethod(responseClass=SampleDto.SampleResponseDto)
    def fromModelToResponseDto(self, model, dto) :
        dto.featureDataList = []
        for featureData in model.featureDataList :
            dto.featureDataList.append(
                FeatureDataDto.FeatureDataResponseDto(
                    value = featureData.value,
                    featureKey = featureData.feature.key,
                    sampleKey = featureData.sample.key
                )
            )
        return dto

    @ConverterMethod()
    def fromModelListToResponseDtoList(self,sampleList):
        responseDtoList = []
        for sample in sampleList :
            responseDtoList.append(self.fromModelToResponseDto(sample))
        return responseDtoList
