from FlaskHelper import Service, ServiceMethod
import Feature, FeatureDto, SampleDto

@Service()
class FeatureService:

    @ServiceMethod()
    def queryAll(self):
        return self.converter.feature.fromModelListToResponseDtoList(self.findAll())

    @ServiceMethod(requestClass=str().__class__)
    def queryByKey(self,key):
        return self.converter.feature.fromModelToResponseDto(self.findByKey(key))

    @ServiceMethod(requestClass=[FeatureDto.FeaturePostRequestDto])
    def create(self,requestDto):
        self.validator.feature.postRequestDto(requestDto)
        newFeature = self.mapper.feature.fromPostDtoToModel(requestDto)
        feature = self.repository.feature.save(newFeature)
        return self.converter.feature.fromModelToResponseDto(feature)

    @ServiceMethod(requestClass=[FeatureDto.FeatureRequestDto, str().__class__])
    def update(self,requestDto,key):
        self.validator.feature.putRequestDto(requestDto,key)
        feature = self.repository.feature.findByKey(key)
        feature = self.mapper.feature.fromRequestDtoToModel(requestDto,feature)
        feature = self.repository.feature.save(feature)
        return self.converter.feature.fromModelToResponseDto(feature)

    @ServiceMethod(requestClass=str().__class__)
    def delete(self,key):
        self.validator.feature.existsByKey(key)
        self.repository.feature.deleteByKey(key)

    @ServiceMethod()
    def findAll(self):
        return self.repository.feature.findAll()

    @ServiceMethod(requestClass=str().__class__)
    def findByKey(self,key):
        self.validator.feature.existsByKey(key)
        return self.repository.feature.findByKey(key)

    @ServiceMethod(requestClass=str().__class__)
    def existsByKey(self, key):
        return self.repository.feature.existsByKey(key)

    @ServiceMethod(requestClass=SampleDto.SamplePostRequestDto)
    def findAllBySamplePostRequestDto(self,dto) :
        self.validator.sample.featureDataPostRequestDtoList(dto.featureDataList)
        return self.findAllByFeatureDataDtoList(dto.featureDataList)

    @ServiceMethod(requestClass=SampleDto.SampleRequestDto)
    def findAllBySampleRequestDto(self,dto) :
        self.validator.sample.featureDataRequestDtoList(dto.featureDataList)
        return self.findAllByFeatureDataDtoList(dto.featureDataList)

    def findAllByFeatureDataDtoList(self, featureDataDtoList):
        featureKeyList = []
        for featureDataPostRequestDto in featureDataDtoList :
            if featureDataPostRequestDto.featureKey :
                featureKeyList.append(featureDataPostRequestDto.featureKey)
        featureList = self.repository.feature.findAllByFeatureKeyIn(featureKeyList)
        self.validator.feature.featureListByfeatureKeyList(featureList, featureKeyList)
        return featureList
