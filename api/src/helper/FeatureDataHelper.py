from FlaskHelper import Helper, HelperMethod
import FeatureData, Feature, Sample, BestFitDto

@Helper()
class FeatureDataHelper:

    @HelperMethod(requestClass=[Feature.Feature, [FeatureData.FeatureData]])
    def getRespectiveFeatureDataByFeature(self, feature, featureDataList):
        for featureData in featureDataList :
            if featureData.feature and feature.key == featureData.feature.key :
                return featureData

    @HelperMethod(requestClass=[int, [FeatureData.FeatureData]])
    def getRespectiveFeatureDataByFeatureId(self, featureId, featureDataList) :
        for featureData in featureDataList :
            if featureData.feature and featureId and featureData.feature.id and featureId == featureData.feature.id :
                return featureData


    @HelperMethod(requestClass=[[Feature.Feature], Sample.Sample])
    def removeRejectedFeatureData(self, featureList, sampleToUpdate):
        featureIdListToRemove = []
        for featureData in sampleToUpdate.featureDataList :
            feature = self.helper.feature.getRespectiveFeatureByFeatureData(featureData, featureList)
            if not feature :
                featureIdListToRemove.append(featureData.feature.id)
        for featureId in featureIdListToRemove :
            featureData = self.helper.featureData.getRespectiveFeatureDataByFeatureId(featureId, sampleToUpdate.featureDataList)
            sampleToUpdate.featureDataList.remove(featureData)

    @HelperMethod(requestClass=[[BestFitDto.BestFitRequestDto]])
    def getFeatureKeyList(self, bestFitList):
        featureKeyList = []
        for bestFit in bestFitList :
            featureKeyList.append(bestFit.featureKey)
        return featureKeyList
