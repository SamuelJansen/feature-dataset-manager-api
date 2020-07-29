from FlaskHelper import Helper, HelperMethod
import FeatureData, Feature

@Helper()
class FeatureDataHelper:

    @HelperMethod(requestClass=[Feature.Feature, [FeatureData.FeatureData]])
    def getRespectiveFeatureDataByFeature(self, feature, featureDataList):
        for featureData in featureDataList :
            if featureData.feature and feature.key == featureData.feature.key :
                return featureData

    @HelperMethod(requestClass=[FeatureData.FeatureData, [Feature.Feature]])
    def getRespectiveFeatureByFeatureData(self, featureData, featureList):
        for feature in featureList :
            if featureData.feature and feature.id and featureData.feature.id and feature.id == featureData.feature.id :
                return feature

    @HelperMethod(requestClass=[int().__class__, [FeatureData.FeatureData]])
    def getRespectiveFeatureDataByFeatureId(self, featureId, featureDataList) :
        for featureData in featureDataList :
            if featureData.feature and featureId and featureData.feature.id and featureId == featureData.feature.id :
                return featureData
