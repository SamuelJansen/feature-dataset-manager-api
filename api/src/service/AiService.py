import numpy
from FlaskHelper import Service, ServiceMethod
from python_helper import Constant, log
import Sample, FeatureData, BestFitDto
import DefaultValue, DataSetKey

@Service()
class AiService:

    @ServiceMethod(requestClass=[FeatureData.FeatureData, int])
    def patchDataValues(self, featureData, value, patchValues=False):
        '''
        It updates the values based on online mean'''
        self.validator.common.isBoolean(patchValues)
        if not featureData.iterationCount :
            featureData.value = DefaultValue.DEFAULT_VALUE
            featureData.iterationCount = DefaultValue.DEFAULT_ITERATION_COUNT
        if not featureData.feature.iterationCount :
            featureData.feature.value = DefaultValue.DEFAULT_VALUE
            featureData.feature.iterationCount = DefaultValue.DEFAULT_ITERATION_COUNT
        if patchValues :
            featureData.iterationCount += 1
            featureData.value += ((value - featureData.value) / featureData.iterationCount)
            featureData.feature.iterationCount += 1
            featureData.feature.value += ((value - featureData.feature.value) / featureData.feature.iterationCount)

    @ServiceMethod(requestClass=[Sample.Sample, int])
    def patchSampleValues(self, sample, value, patchValues=False):
        '''
        It updates the values based on online mean'''
        self.validator.common.isBoolean(patchValues)
        if not sample.iterationCount :
            sample.value = DefaultValue.DEFAULT_VALUE
            sample.iterationCount = DefaultValue.DEFAULT_ITERATION_COUNT
        if patchValues :
            sample.iterationCount += 1
            sample.value += ((value - sample.value) / sample.iterationCount)

    @ServiceMethod(requestClass=[[BestFitDto.BestFitRequestDto]])
    def getTargetData(self, bestFitList):
        return [DefaultValue.MAXIMUM_DATA_VALUE for x in bestFitList]

    @ServiceMethod(requestClass=[[int], set])
    def getBestFit(self, targetData, dataSet):
        '''
        It calculates the nearest dataset point of a target data point
        measuring its Euclidian Distance from a data set'''
        log.debug(AiService, f'Querying ...')
        targetArray = numpy.asarray(targetData)
        dataSetMatrix = numpy.asarray([data[DataSetKey.VALUE_LIST] for data in dataSet.values()])
        euclidianDistanceList = numpy.sum((targetArray - dataSetMatrix)**2, axis=1)
        bestFitIndex = numpy.argmin(euclidianDistanceList)
        bestFit = dataSet[list(dataSet.values())[bestFitIndex][DataSetKey.SAMPLE].key][DataSetKey.SAMPLE]
        print(dataSetMatrix)
        log.debug(AiService,f'Best fit index: {bestFitIndex}')
        log.debug(AiService,f'Optimum match: {bestFit}')
        return bestFit
