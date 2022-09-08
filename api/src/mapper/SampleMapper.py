from python_helper import ObjectHelper
from python_framework import Mapper, MapperMethod

from Sample import Sample
from Feature import Feature

from dto.SampleDto import SampleRequestDto
from dto.BestFitDto import BestFitRequestDto
from dto.FeatureDataDto import FeatureDataRequestDto

import DefaultValue

@Mapper()
class SampleMapper:

    @MapperMethod(requestClass=[SampleRequestDto, [Feature], str], responseClass=Sample)
    def fromPostRequestDtoToModel(self, dto, featureList, key, model):
        self.validator.sample.listLengthAreEqualsInSampleMapping(featureList, model.featureDataList)
        model.key = key
        model.featureDataList = []
        self.overrideModelValues(dto, model)
        return model

    @MapperMethod(requestClass=[[FeatureDataRequestDto], str])
    def overrideFeatureDataRequestDtoValues(self, featureDataList, key):
        for featureData in featureDataList :
            if not featureData.sampleKey:
                featureData.sampleKey = key

    @MapperMethod(requestClass=[SampleRequestDto, Sample])
    def overrideModelValues(self, dto, model):
        if ObjectHelper.isNotNone(dto) and ObjectHelper.isNotNone(dto.label):
            model.label = dto.label
