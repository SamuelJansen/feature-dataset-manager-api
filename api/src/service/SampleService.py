from FlaskHelper import Service, ServiceMethod
import Sample, SampleDto, Feature, FeatureData, BestFitDto
import DefaultValue

@Service()
class SampleService:

    @ServiceMethod(requestClass=[[BestFitDto.BestFitRequestDto], int])
    def queryBestFit(self, bestFitList, amount):
        self.validator.sample.bestFitRequestDtoList(bestFitList)
        featureKeyList = self.helper.featureData.getFeatureKeyList(bestFitList)
        sampleList = self.repository.sample.findAllByFeatureKeyIn(featureKeyList)
        dataSet = self.helper.sample.getSampleDataSet(sampleList, bestFitList)
        targetData = self.service.ai.getTargetData(bestFitList)
        bestFit = self.service.ai.getBestFit(targetData, dataSet)
        return self.converter.sample.fromModelToResponseDto(bestFit)

    @ServiceMethod()
    def queryAll(self):
        return self.converter.sample.fromModelListToResponseDtoList(self.findAll())

    @ServiceMethod(requestClass=str)
    def queryByKey(self, key):
        sample = self.findByKey(key)
        return self.converter.sample.fromModelToResponseDto(sample)

    @ServiceMethod(requestClass=[SampleDto.SampleRequestDto, str])
    def create(self, dto, key):
        self.validator.sample.postRequestDto(dto, key)
        self.mapper.sample.overrideFeatureDataRequestDtoValues(dto.featureDataList, key)
        featureList = self.service.feature.findAllBySampleRequestDto(dto)
        newSample = self.mapper.sample.fromPostRequestDtoToModel(dto, featureList, DefaultValue.DEFAULT_VALUE, key)
        sample = self.repository.sample.save(newSample)
        return self.converter.sample.fromModelToResponseDto(sample)

    @ServiceMethod(requestClass=[SampleDto.SampleRequestDto, str])
    def update(self, dto, key):
        self.validator.sample.putRequestDto(dto, key)
        self.mapper.sample.overrideFeatureDataRequestDtoValues(dto.featureDataList, key)
        featureList = self.service.feature.findAllBySampleRequestDto(dto)
        sampleToUpdate = self.findByKey(key)
        self.mapper.sample.overrideModelValues(dto, featureList, DefaultValue.DEFAULT_VALUE, sampleToUpdate)
        self.helper.featureData.removeRejectedFeatureData(featureList, sampleToUpdate)
        sample = self.repository.sample.save(sampleToUpdate)
        return self.converter.sample.fromModelToResponseDto(sample)

    @ServiceMethod(requestClass=[SampleDto.SampleRequestDto, str, int])
    def patch(self, dto, key, value):
        self.validator.sample.patchRequestDto(dto, key, value)
        self.mapper.sample.overrideFeatureDataRequestDtoValues(dto.featureDataList, key)
        featureList = self.service.feature.findAllBySampleRequestDto(dto)
        sampleToPatch = self.findByKey(key)
        self.mapper.sample.overrideModelValues(dto, featureList, value, sampleToPatch, patchValues=True)
        sample = self.repository.sample.save(sampleToPatch)
        return self.converter.sample.fromModelToResponseDto(sample)

    @ServiceMethod(requestClass=str)
    def delete(self,key):
        self.validator.sample.existsByKey(key)
        self.repository.sample.deleteByKey(key)

    @ServiceMethod()
    def findAll(self):
        return self.repository.sample.findAll()

    @ServiceMethod(requestClass=str)
    def findByKey(self,key):
        self.validator.sample.existsByKey(key)
        return self.repository.sample.findByKey(key)

    @ServiceMethod(requestClass=str)
    def existsByKey(self, key):
        return self.repository.sample.existsByKey(key)
