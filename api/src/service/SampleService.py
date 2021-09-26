from python_helper import ObjectHelper
from python_framework import Service, ServiceMethod

from Sample import Sample
from Feature import Feature
from FeatureData import FeatureData

from dto.SampleDto import SampleRequestDto
from dto.BestFitDto import BestFitRequestDto

import DefaultValue

@Service()
class SampleService:

    @ServiceMethod(requestClass=[[BestFitRequestDto], int])
    def queryBestFitList(self, bestFitList, amount):
        self.validator.sample.bestFitRequestDtoList(bestFitList, amount)
        featureKeyList = self.helper.featureData.getFeatureKeyList(bestFitList)
        modelList = self.repository.sample.findAllByFeatureKeyIn(featureKeyList)
        dataSet = self.helper.sample.getSampleDataSet(modelList, bestFitList)
        targetData = self.service.ai.getTargetData(bestFitList)
        bestFitList = self.service.ai.getBestFitList(targetData, dataSet, amount)
        return self.converter.sample.fromModelListToBestFitResponseDtoList(bestFitList)

    @ServiceMethod()
    def queryAll(self):
        return self.converter.sample.fromModelListToResponseDtoList(self.findAll())

    @ServiceMethod(requestClass=str)
    def queryByKey(self, key):
        model = self.findByKey(key)
        return self.converter.sample.fromModelToResponseDto(model)

    @ServiceMethod(requestClass=[SampleRequestDto, str])
    def create(self, dto, key):
        self.validator.sample.postRequestDto(dto, key)
        self.mapper.sample.overrideFeatureDataRequestDtoValues(dto.featureDataList, key)
        featureList = self.service.feature.findAllBySampleRequestDto(dto)
        newModel = self.mapper.sample.fromPostRequestDtoToModel(dto, featureList, key)
        self.patchFeatureDataList(featureList, newModel)
        self.repository.sample.save(newModel)
        return self.converter.sample.fromModelToResponseDto(newModel)

    @ServiceMethod(requestClass=[SampleRequestDto, str])
    def update(self, dto, key):
        self.validator.sample.putRequestDto(dto, key)
        self.mapper.sample.overrideFeatureDataRequestDtoValues(dto.featureDataList, key)
        featureList = self.service.feature.findAllBySampleRequestDto(dto)
        model = self.findByKey(key)
        self.mapper.sample.overrideModelValues(dto, model)
        self.patchFeatureDataList(featureList, model)
        self.repository.sample.save(model)
        return self.converter.sample.fromModelToResponseDto(model)

    @ServiceMethod(requestClass=[SampleRequestDto, str, int])
    def patch(self, dto, key, value):
        self.validator.sample.patchRequestDto(dto, key, value)
        self.mapper.sample.overrideFeatureDataRequestDtoValues(dto.featureDataList, key)
        featureList = self.service.feature.findAllBySampleRequestDto(dto)
        model = self.findByKey(key)
        self.mapper.sample.overrideModelValues(dto, model)
        self.patchFeatureDataList(featureList, model)
        self.service.ai.patchSample(featureList, model, value)
        self.repository.sample.save(model)
        return self.converter.sample.fromModelToResponseDto(model)

    @ServiceMethod(requestClass=[[Feature], Sample])
    def patchFeatureDataList(self, featureList, model):
        for feature in featureList :
            featureData = self.helper.featureData.getRespectiveFeatureDataByFeature(feature, model.featureDataList)
            if ObjectHelper.isNone(featureData) :
                featureData = FeatureData()
            featureData.sample = model
            featureData.feature = feature
            if ObjectHelper.isNone(featureData.iterationCount) :
                featureData.value = DefaultValue.DEFAULT_VALUE
                featureData.iterationCount = DefaultValue.DEFAULT_ITERATION_COUNT
            if ObjectHelper.isNone(featureData.feature.iterationCount) :
                featureData.feature.value = DefaultValue.DEFAULT_VALUE
                featureData.feature.iterationCount = DefaultValue.DEFAULT_ITERATION_COUNT
            if featureData not in model.featureDataList:
                model.featureDataList.append(featureData)
        if ObjectHelper.isNone(model.iterationCount) :
            model.value = DefaultValue.DEFAULT_VALUE
            model.iterationCount = DefaultValue.DEFAULT_ITERATION_COUNT

    @ServiceMethod(requestClass=str)
    def delete(self,key):
        self.validator.sample.existsByKey(key)
        self.repository.sample.deleteByKey(key)

    @ServiceMethod()
    def findAll(self):
        return self.repository.sample.findAll()

    @ServiceMethod(requestClass=str)
    def findByKey(self,key):
        self.validator.sample.existsByKey(key)
        return self.repository.sample.findByKey(key)

    @ServiceMethod(requestClass=str)
    def existsByKey(self, key):
        return self.repository.sample.existsByKey(key)
