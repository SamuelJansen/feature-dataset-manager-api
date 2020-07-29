from FlaskHelper import Mapper, MapperMethod
import Sample, SampleDto, FeatureData, Feature, FeatureDataDto
import GlobalException, DefaultValues

@Mapper()
class SampleMapper:

    @MapperMethod(requestClass=[SampleDto.SamplePostRequestDto, [Feature.Feature]], responseClass=Sample.Sample)
    def fromPostRequestDtoToModel(self, samplePostRequestDto, featureList, model) :
        model.value = DefaultValues.DEFAULT_VALUE
        model.iterationCount = DefaultValues.DEFAULT_ITERATION_COUNT
        self.validator.sample.listLengthAreEqualsInSampleMapping(featureList, list(model.featureDataList))
        for index in range(len(model.featureDataList)) :
            self.overrideFeatureDataValues(model.featureDataList[index], featureList[index])
        return model

    @MapperMethod(requestClass=[[FeatureDataDto.FeatureDataPostRequestDto], str().__class__])
    def overrideFeatureDataListValues(self, featureDataList, key):
        for featureData in featureDataList :
            if not featureData.sampleKey :
                featureData.sampleKey = key

    @MapperMethod(requestClass=[[FeatureDataDto.FeatureDataRequestDto], str().__class__])
    def overrideFeatureDataRequestDtoValues(self, featureDataList, key) :
        for featureData in featureDataList :
            if not featureData.sampleKey :
                featureData.sampleKey = key

    @MapperMethod(requestClass=[SampleDto.SampleRequestDto, [Feature.Feature], Sample.Sample])
    def overrideValues(self, dto, featureList, model):
        model.label = dto.label
        for feature in featureList :
            featureData = self.getRespectiveFeatureData(feature, model.featureDataList)
            if not featureData :
                featureData = FeatureData.FeatureData()
            self.service.sample.updateFeatureDataValues(dto, featureData, feature, sample=model)

    @MapperMethod(requestClass=Feature.Feature)
    def getRespectiveFeatureData(self, feature, featureDataList):
        for featureData in featureDataList :
            if featureData.feature and feature.key == featureData.feature.key :
                return featureData
