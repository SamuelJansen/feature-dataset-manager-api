from FlaskHelper import Service, ServiceMethod
import FeatureData, FeatureDataDto

@Service()
class FeatureDataService:

    @ServiceMethod(requestClass=[str().__class__, str().__class__])
    def queryByFeatureKeyAndSampleKey(self, featureKey, sampleKey):
        featureData = self.findByFeatureKeyAndSampleKey(featureKey, sampleKey)
        return self.converter.featureData.fromModelToResponseDto(featureData)

    @ServiceMethod(requestClass=[str().__class__, str().__class__])
    def deleteByFeatureKeyAndSampleKey(self, featureKey, sampleKey):
        self.validator.featureData.byFeatureKeyAndSampleKey(featureKey, sampleKey)
        self.repository.featureData.deleteByFeatureKeyAndSampleKey(featureKey, sampleKey)

    @ServiceMethod(requestClass=str().__class__)
    def queryAllByFeatureKey(self, featureKey):
        print(featureKey)
        featureKeyList = self.findAllByFeatureKey(featureKey)
        print(featureKeyList)
        return self.converter.featureData.fromModelListToResponseDtoList(featureKeyList)

    @ServiceMethod(requestClass=[str().__class__, str().__class__])
    def findByFeatureKeyAndSampleKey(self, featureKey, sampleKey):
        self.validator.featureData.existsByFeatureKeyAndSampleKey(featureKey, sampleKey)
        return self.repository.featureData.findByFeatureKeyAndSampleKey(featureKey, sampleKey)

    @ServiceMethod(requestClass=str().__class__)
    def findAllByFeatureKey(self, featureKey):
        self.validator.featureData.featureKeyNotNull(featureKey)
        print(featureKey)
        return self.repository.featureData.findAllByFeatureKey(featureKey)

    @ServiceMethod(requestClass=str().__class__)
    def findAllBySampleKey(self, sampleKey):
        self.validator.featureData.sampleKeyNotNull(sampleKey)
        return self.repository.featureData.findAllBySampleKey(sampleKey)

    @ServiceMethod(requestClass=[str().__class__, str().__class__])
    def existsByFeatureKeyAndSampleKey(self, featureKey, sampleKey):
        return self.repository.featureData.existsByFeatureKeyAndSampleKey(featureKey, sampleKey)
