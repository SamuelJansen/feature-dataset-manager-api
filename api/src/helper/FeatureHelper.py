from python_framework import Helper, HelperMethod
import FeatureData, Feature

@Helper()
class FeatureHelper:

    @HelperMethod(requestClass=[FeatureData.FeatureData, [Feature.Feature]])
    def getRespectiveFeatureByFeatureData(self, featureData, featureList):
        for feature in featureList :
            if featureData.feature and feature.id and featureData.feature.id and feature.id == featureData.feature.id :
                return feature
