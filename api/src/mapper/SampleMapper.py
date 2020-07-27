from FlaskHelper import Mapper, MapperMethod
import Sample, SampleDto, FeatureData, Feature, GlobalException

DEFAULT_VALUE = 3

@Mapper()
class SampleMapper:

    @MapperMethod(responseClass=Sample.Sample)
    def fromPostRequestDtoToModel(self, samplePostRequestDto, featureList, model) :
        model.value = DEFAULT_VALUE
        self.validator.sample.listLengthAreEqualsInSampleMapping(featureList, list(model.featureDataList))
        for index in range(len(model.featureDataList)) :
            self.overrideFeatureDataValues(model.featureDataList[index], featureList[index])
        return model

    @MapperMethod()
    def overrideFeatureDataListValues(self, featureDataList, key):
        for featureData in featureDataList :
            if not featureData.sampleKey :
                featureData.sampleKey = key

    @MapperMethod(requestClass=[SampleDto.SampleRequestDto, list().__class__, Sample.Sample])
    def overrideValues(self, dto, featureList, model):
        model.label = dto.label
        for feature in featureList :
            featureData = self.getRespectiveFeatureData(feature, model.featureDataList)
            if not featureData :
                featureData = FeatureData.FeatureData(sample=model)
            self.overrideFeatureDataValues(featureData, feature)

    @MapperMethod(requestClass=[FeatureData.FeatureData, Feature.Feature])
    def overrideFeatureDataValues(self, featureData, feature, sample=None):
        featureData.feature = feature
        if sample :
            featureData.sample = sample
        featureData.value = DEFAULT_VALUE

    @MapperMethod(requestClass=Feature.Feature)
    def getRespectiveFeatureData(self, feature, featureDataList):
        for featureData in featureDataList :
            if featureData.feature and feature.key == featureData.feature.key :
                return featureData
