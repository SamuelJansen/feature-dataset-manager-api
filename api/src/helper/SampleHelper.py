from python_framework import Helper, HelperMethod

from Sample import Sample

from dto.BestFitDto import BestFitRequestDto

import DefaultValue, DataSetKey

@Helper()
class SampleHelper:

    @HelperMethod(requestClass=[[Sample], [BestFitRequestDto]])
    def getSampleDataSet(self, sampleList, bestFitList):
        dataSet = {}
        for sample in sampleList :
            dataSet[sample.key] = {
                DataSetKey.SAMPLE : sample,
                DataSetKey.VALUE_LIST : []
            }
            for bestFit in bestFitList :
                dataSet[sample.key][DataSetKey.VALUE_LIST].append(self.getSampleDataValue(sample, bestFit))
        return dataSet

    @HelperMethod(requestClass=[Sample, BestFitRequestDto])
    def getSampleDataValue(self, sample, bestFit):
        for featureData in sample.featureDataList :
            if featureData.feature.key == bestFit.featureKey:
                return featureData.value
        return DefaultValue.DEFAULT_MISSING_DATA_VALUE
