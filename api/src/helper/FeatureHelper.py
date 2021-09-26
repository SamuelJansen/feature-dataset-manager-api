from python_framework import Helper, HelperMethod

from Feature import Feature
from FeatureData import FeatureData

@Helper()
class FeatureHelper:

    @HelperMethod(requestClass=[FeatureData, [Feature]])
    def getRespectiveFeatureByFeatureData(self, featureData, featureList):
        for feature in featureList :
            if featureData.feature and feature.id and featureData.feature.id and feature.id == featureData.feature.id :
                return feature
