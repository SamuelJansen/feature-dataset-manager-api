from FlaskHelper import Service, ServiceMethod
import Sample, SampleDto, Feature, FeatureData
import DefaultValues

@Service()
class SampleService:

    @ServiceMethod(requestClass=[FeatureData.FeatureData, int().__class__])
    def patchDataValues(self, featureData, value, patchValues=False):
        self.validator.common.isBoolean(patchValues)
        if not featureData.iterationCount :
            featureData.value = DefaultValues.DEFAULT_VALUE
            featureData.iterationCount = DefaultValues.DEFAULT_ITERATION_COUNT
        if not featureData.feature.iterationCount :
            featureData.feature.value = DefaultValues.DEFAULT_VALUE
            featureData.feature.iterationCount = DefaultValues.DEFAULT_ITERATION_COUNT
        if patchValues :
            featureData.iterationCount += 1
            featureData.value += ((value - featureData.value) / featureData.iterationCount)
            featureData.feature.iterationCount += 1
            featureData.feature.value += ((value - featureData.feature.value) / featureData.feature.iterationCount)

    @ServiceMethod(requestClass=[Sample.Sample, int().__class__])
    def patchSampleValues(self, sample, value, patchValues=False):
        self.validator.common.isBoolean(patchValues)
        if not sample.iterationCount :
            sample.value = DefaultValues.DEFAULT_VALUE
            sample.iterationCount = DefaultValues.DEFAULT_ITERATION_COUNT
        if patchValues :
            sample.iterationCount += 1
            sample.value += ((value - sample.value) / sample.iterationCount)

    @ServiceMethod(requestClass=[[Feature.Feature], Sample.Sample])
    def removeRejectedFeatureData(self, featureList, sampleToUpdate):
        featureIdListToRemove = []
        for featureData in sampleToUpdate.featureDataList :
            feature = self.helper.featureData.getRespectiveFeatureByFeatureData(featureData, featureList)
            if not feature :
                featureIdListToRemove.append(featureData.feature.id)
        for featureId in featureIdListToRemove :
            featureData = self.helper.featureData.getRespectiveFeatureDataByFeatureId(featureId, sampleToUpdate.featureDataList)
            sampleToUpdate.featureDataList.remove(featureData)

    @ServiceMethod()
    def queryAll(self):
        return self.converter.sample.fromModelListToResponseDtoList(self.findAll())

    @ServiceMethod(requestClass=str().__class__)
    def queryByKey(self, key):
        sample = self.findByKey(key)
        return self.converter.sample.fromModelToResponseDto(sample)

    @ServiceMethod(requestClass=[SampleDto.SampleRequestDto, str().__class__])
    def create(self, dto, key):
        self.validator.sample.postRequestDto(dto, key)
        self.mapper.sample.overrideFeatureDataRequestDtoValues(dto.featureDataList, key)
        featureList = self.service.feature.findAllBySampleRequestDto(dto)
        newSample = self.mapper.sample.fromPostRequestDtoToModel(dto, featureList, DefaultValues.DEFAULT_VALUE, key)
        sample = self.repository.sample.save(newSample)
        return self.converter.sample.fromModelToResponseDto(sample)

    @ServiceMethod(requestClass=[SampleDto.SampleRequestDto, str().__class__])
    def update(self, dto, key):
        self.validator.sample.putRequestDto(dto, key)
        self.mapper.sample.overrideFeatureDataRequestDtoValues(dto.featureDataList, key)
        featureList = self.service.feature.findAllBySampleRequestDto(dto)
        sampleToUpdate = self.findByKey(key)
        self.mapper.sample.overrideValues(dto, featureList, DefaultValues.DEFAULT_VALUE, sampleToUpdate)
        self.removeRejectedFeatureData(featureList, sampleToUpdate)
        sample = self.repository.sample.save(sampleToUpdate)
        return self.converter.sample.fromModelToResponseDto(sample)

    @ServiceMethod(requestClass=[SampleDto.SampleRequestDto, str().__class__, int().__class__])
    def patch(self, dto, key, value):
        self.validator.sample.patchRequestDto(dto, key, value)
        self.mapper.sample.overrideFeatureDataRequestDtoValues(dto.featureDataList, key)
        featureList = self.service.feature.findAllBySampleRequestDto(dto)
        sampleToPatch = self.findByKey(key)
        self.mapper.sample.overrideValues(dto, featureList, value, sampleToPatch, patchValues=True)
        sample = self.repository.sample.save(sampleToPatch)
        return self.converter.sample.fromModelToResponseDto(sample)

    @ServiceMethod(requestClass=str().__class__)
    def delete(self,key):
        self.validator.sample.existsByKey(key)
        self.repository.sample.deleteByKey(key)

    @ServiceMethod()
    def findAll(self):
        return self.repository.sample.findAll()

    @ServiceMethod(requestClass=str().__class__)
    def findByKey(self,key):
        self.validator.sample.existsByKey(key)
        return self.repository.sample.findByKey(key)

    @ServiceMethod(requestClass=str().__class__)
    def existsByKey(self, key):
        return self.repository.sample.existsByKey(key)
