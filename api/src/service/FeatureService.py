from python_framework import Service, ServiceMethod

from dto.FeatureDto import FeatureRequestDto
from dto.SampleDto import SampleRequestDto

@Service()
class FeatureService:

    @ServiceMethod()
    def queryAll(self):
        return self.converter.feature.fromModelListToResponseDtoList(self.findAll())

    @ServiceMethod(requestClass=str)
    def queryByKey(self,key):
        return self.converter.feature.fromModelToResponseDto(self.findByKey(key))

    @ServiceMethod(requestClass=[FeatureRequestDto, str])
    def create(self, dto, key):
        self.validator.feature.postRequestDto(dto, key)
        feature = self.mapper.feature.fromPostRequestDtoToModel(dto, key)
        self.repository.feature.save(feature)
        return self.converter.feature.fromModelToResponseDto(feature)

    @ServiceMethod(requestClass=[FeatureRequestDto, str])
    def update(self, dto, key):
        self.validator.feature.putRequestDto(dto, key)
        feature = self.repository.feature.findByKey(key)
        self.mapper.feature.overrideModelFromRequestDto(dto, model)
        self.repository.feature.save(feature)
        return self.converter.feature.fromModelToResponseDto(feature)

    @ServiceMethod(requestClass=str)
    def delete(self,key):
        self.validator.feature.existsByKey(key)
        self.repository.feature.deleteByKey(key)

    @ServiceMethod()
    def findAll(self):
        return self.repository.feature.findAll()

    @ServiceMethod(requestClass=str)
    def findByKey(self,key):
        self.validator.feature.existsByKey(key)
        return self.repository.feature.findByKey(key)

    @ServiceMethod(requestClass=str)
    def existsByKey(self, key):
        return self.repository.feature.existsByKey(key)

    @ServiceMethod(requestClass=SampleRequestDto)
    def findAllBySampleRequestDto(self,dto):
        self.validator.sample.featureDataRequestDtoList(dto.featureDataList)
        featureKeyList = [featureDataRequestDto.featureKey for featureDataRequestDto in dto.featureDataList if featureDataRequestDto.featureKey]
        featureList = self.repository.feature.findAllByFeatureKeyIn(featureKeyList)
        self.validator.feature.featureListByfeatureKeyList(featureList, featureKeyList)
        return featureList
