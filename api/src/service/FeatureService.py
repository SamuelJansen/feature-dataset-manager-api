from FlaskManager import Service, ServiceMethod
import Feature, FeatureDto, FeatureDataDto, SampleDto

@Service()
class FeatureService:

    @ServiceMethod()
    def queryAll(self):
        return self.converter.feature.fromModelListToResponseDtoList(self.findAll())

    @ServiceMethod(requestClass=str)
    def queryByKey(self,key):
        return self.converter.feature.fromModelToResponseDto(self.findByKey(key))

    @ServiceMethod(requestClass=[FeatureDto.FeatureRequestDto, str])
    def create(self, dto, key):
        self.validator.feature.postRequestDto(dto, key)
        newFeature = self.mapper.feature.fromPostRequestDtoToModel(dto, key)
        feature = self.repository.feature.save(newFeature)
        return self.converter.feature.fromModelToResponseDto(feature)

    @ServiceMethod(requestClass=[FeatureDto.FeatureRequestDto, str])
    def update(self, dto, key):
        self.validator.feature.putRequestDto(dto,key)
        feature = self.repository.feature.findByKey(key)
        feature = self.mapper.feature.fromRequestDtoToModel(dto,feature)
        feature = self.repository.feature.save(feature)
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

    @ServiceMethod(requestClass=SampleDto.SampleRequestDto)
    def findAllBySampleRequestDto(self,dto) :
        self.validator.sample.featureDataRequestDtoList(dto.featureDataList)
        featureKeyList = []
        for featureDataRequestDto in dto.featureDataList :
            if featureDataRequestDto.featureKey :
                featureKeyList.append(featureDataRequestDto.featureKey)
        featureList = self.repository.feature.findAllByFeatureKeyIn(featureKeyList)
        self.validator.feature.featureListByfeatureKeyList(featureList, featureKeyList)
        return featureList
