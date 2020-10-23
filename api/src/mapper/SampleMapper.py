from python_framework import Mapper, MapperMethod
import Sample, SampleDto, FeatureData, Feature, FeatureDataDto
import DefaultValue

@Mapper()
class SampleMapper:

    @MapperMethod(requestClass=[SampleDto.SampleRequestDto, [Feature.Feature], int], responseClass=Sample.Sample)
    def fromPostRequestDtoToModel(self, dto, featureList, value, key, model) :
        self.validator.sample.listLengthAreEqualsInSampleMapping(featureList, model.featureDataList)
        model.key = key
        model.featureDataList = []
        self.overrideModelValues(dto, featureList, value, model)
        return model

    @MapperMethod(requestClass=[[FeatureDataDto.FeatureDataRequestDto], str])
    def overrideFeatureDataRequestDtoValues(self, featureDataList, key) :
        for featureData in featureDataList :
            if not featureData.sampleKey :
                featureData.sampleKey = key

    @MapperMethod(requestClass=[SampleDto.SampleRequestDto, [Feature.Feature], Sample.Sample])
    def overrideFeatureData(self, dto, featureList, model):
        model.label = dto.label
        for feature in featureList :
            featureData = self.helper.featureData.getRespectiveFeatureDataByFeature(feature, model.featureDataList)
            if not featureData :
                featureData = FeatureData.FeatureData()
                featureData.sample = model
            featureData.feature = feature

    @MapperMethod(requestClass=[SampleDto.SampleRequestDto, [Feature.Feature], int, Sample.Sample])
    def overrideModelValues(self, dto, featureList, value, model, patchValues=False):
        if dto.label :
            model.label = dto.label
        for feature in featureList :
            featureData = self.helper.featureData.getRespectiveFeatureDataByFeature(feature, model.featureDataList)
            if not featureData :
                featureData = FeatureData.FeatureData()
                featureData.sample = model
                featureData.feature = feature
            self.service.ai.patchDataValues(featureData, value, patchValues=patchValues)
        self.service.ai.patchSampleValues(model, value, patchValues=patchValues)
