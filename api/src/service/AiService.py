import numpy
from python_framework import Service, ServiceMethod
from python_helper import Constant, log

from Sample import Sample
from Feature import Feature
from FeatureData import FeatureData

from dto.BestFitDto import BestFitRequestDto

import DefaultValue, DataSetKey

@Service()
class AiService:

    @ServiceMethod(requestClass=[FeatureData, int])
    def patchFeatureData(self, featureData, value):
        featureData.iterationCount += 1
        featureData.value += ((value - featureData.value) / featureData.iterationCount)
        featureData.feature.iterationCount += 1
        featureData.feature.value += ((value - featureData.feature.value) / featureData.feature.iterationCount)

    @ServiceMethod(requestClass=[[Feature], Sample, int])
    def patchSample(self, featureList, sample, value):
        for feature in featureList :
            featureData = self.helper.featureData.getRespectiveFeatureDataByFeature(feature, sample.featureDataList)
            self.validator.featureData.validateModelNotNone(featureData)
            self.patchFeatureData(featureData, value)
        sample.iterationCount += 1
        sample.value += ((value - sample.value) / sample.iterationCount)

    @ServiceMethod(requestClass=[[BestFitRequestDto]])
    def getTargetData(self, bestFitList):
        return [DefaultValue.MAXIMUM_DATA_VALUE for x in bestFitList]

    @ServiceMethod(requestClass=[[int], set, int])
    def getBestFitList(self, targetData, dataSet, amount):
        if not dataSet or 0 == len(dataSet):
            return []
        log.debug(AiService, f'Querying {amount} samples ...')
        targetArray = numpy.asarray(targetData)
        dataSetMatrix = numpy.asarray([data[DataSetKey.VALUE_LIST] for data in dataSet.values()])
        euclidianDistanceList = numpy.asarray(numpy.sum((targetArray - dataSetMatrix)**2, axis=1))
        log.debug(AiService, f'euclidianDistanceList = {euclidianDistanceList}')
        bestFitIndexList = numpy.argsort(euclidianDistanceList)
        log.debug(AiService, f'bestFitIndexList = {bestFitIndexList}')
        log.debug(AiService, f'dataSetMatrix = {dataSetMatrix}')
        bestFitList = []
        for bestFitIndex in bestFitIndexList[:amount] :
            bestFit = dataSet[list(dataSet.values())[bestFitIndex][DataSetKey.SAMPLE].key][DataSetKey.SAMPLE]
            bestFitList.append(bestFit)
        log.debug(AiService,f'Optimum match: {bestFitList}')
        return bestFitList
