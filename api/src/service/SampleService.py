from FlaskHelper import Service, ServiceMethod
import Sample, SampleDto, FeatureData, Feature
import DefaultValues

@Service()
class SampleService:

    @ServiceMethod(requestClass=[SampleDto.SampleRequestDto, FeatureData.FeatureData, Feature.Feature])
    def updateFeatureDataValues(self, dto, featureData, feature, sample=None):
        featureData.feature = feature
        self.validator.sample.model(sample)
        if sample :
            featureData.sample = sample
        if featureData.iterationCount :
            featureData.iterationCount += 1
            featureData.value += ((dto.value - featureData.value) / featureData.iterationCount)
            featureData.feature.iterationCount += 1
            featureData.feature.value += ((dto.value - featureData.feature.value) / featureData.feature.iterationCount)
            featureData.sample.iterationCount += 1
            featureData.sample.value += ((dto.value - featureData.sample.value) / featureData.sample.iterationCount)
        else :
            featureData.value = DefaultValues.DEFAULT_VALUE
            featureData.iterationCount = DefaultValues.DEFAULT_ITERATION_COUNT

    @ServiceMethod()
    def queryAll(self):
        return self.converter.sample.fromModelListToResponseDtoList(self.findAll())

    @ServiceMethod(requestClass=str().__class__)
    def queryByKey(self,key):
        sample = self.findByKey(key)
        return self.converter.sample.fromModelToResponseDto(sample)

    @ServiceMethod(requestClass=[SampleDto.SamplePostRequestDto])
    def create(self,dto):
        self.validator.sample.postRequestDto(dto)
        self.mapper.sample.overrideFeatureDataListValues(dto.featureDataList, dto.key)
        featureList = self.service.feature.findAllBySamplePostRequestDto(dto)
        newSample = self.mapper.sample.fromPostRequestDtoToModel(dto, featureList)
        sample = self.repository.sample.save(newSample)
        return self.converter.sample.fromModelToResponseDto(sample)

    @ServiceMethod(requestClass=[SampleDto.SampleRequestDto, str().__class__])
    def update(self, dto, key):
        self.validator.sample.putRequestDto(dto, key)
        self.mapper.sample.overrideFeatureDataRequestDtoValues(dto.featureDataList, key)
        featureList = self.service.feature.findAllBySampleRequestDto(dto)
        sampleToUpdate = self.findByKey(key)
        self.mapper.sample.overrideValues(dto, featureList, sampleToUpdate)
        sample = self.repository.sample.save(sampleToUpdate)
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
