from python_framework import Service, ServiceMethod

from FeatureData import FeatureData

@Service()
class FeatureDataService:

    # @ServiceMethod(requestClass=[str, str])
    # def createNewFeatureData(self, featureKey, sampleKey):
    #     if not self.existsByFeatureKeyAndSampleKey(featureKey, sampleKey):
    #         feature = self.service.feature.findByKey(featureKey)
    #         sample = self.service.sample.findByKey(sampleKey)
    #         model = FeatureData()
    #     self.patchFeatureData(model)

    @ServiceMethod(requestClass=[str, str])
    def queryByFeatureKeyAndSampleKey(self, featureKey, sampleKey):
        featureData = self.findByFeatureKeyAndSampleKey(featureKey, sampleKey)
        return self.converter.featureData.fromModelToResponseDto(featureData)

    @ServiceMethod(requestClass=[str, str])
    def deleteByFeatureKeyAndSampleKey(self, featureKey, sampleKey):
        self.validator.featureData.byFeatureKeyAndSampleKey(featureKey, sampleKey)
        self.repository.featureData.deleteByFeatureKeyAndSampleKey(featureKey, sampleKey)

    @ServiceMethod(requestClass=str)
    def queryAllByFeatureKey(self, featureKey):
        featureKeyList = self.findAllByFeatureKey(featureKey)
        return self.converter.featureData.fromModelListToResponseDtoList(featureKeyList)

    @ServiceMethod(requestClass=[str, str])
    def findByFeatureKeyAndSampleKey(self, featureKey, sampleKey):
        self.validator.featureData.existsByFeatureKeyAndSampleKey(featureKey, sampleKey)
        return self.repository.featureData.findByFeatureKeyAndSampleKey(featureKey, sampleKey)

    @ServiceMethod(requestClass=str)
    def findAllByFeatureKey(self, featureKey):
        self.validator.common.pathVariableNotNull(featureKey, 'featureKey')
        return self.repository.featureData.findAllByFeatureKey(featureKey)

    @ServiceMethod(requestClass=str)
    def findAllBySampleKey(self, sampleKey):
        self.validator.common.pathVariableNotNull(sampleKey, 'sampleKey')
        return self.repository.featureData.findAllBySampleKey(sampleKey)

    @ServiceMethod(requestClass=[str, str])
    def existsByFeatureKeyAndSampleKey(self, featureKey, sampleKey):
        return self.repository.featureData.existsByFeatureKeyAndSampleKey(featureKey, sampleKey)
