from FlaskHelper import Service, ServiceMethod
import Sample, SampleDto

@Service()
class SampleService:

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
        self.mapper.sample.overrideFeatureDataListValues(dto.featureDataList, key)
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
