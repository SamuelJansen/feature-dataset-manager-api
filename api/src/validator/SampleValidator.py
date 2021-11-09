from python_framework import Validator, ValidatorMethod, GlobalException, HttpStatus

from Feature import Feature
from FeatureData import FeatureData

from dto.SampleDto import SampleRequestDto
from dto.FeatureDataDto import FeatureDataRequestDto
from dto.BestFitDto import BestFitRequestDto

import DefaultValue

@Validator()
class SampleValidator:

    @ValidatorMethod(requestClass=SampleRequestDto)
    def postRequestDto(self, dto, key):
        self.notExistsByKey(key)
        if not len(self.service.featureData.findAllBySampleKey(key)) == 0 :
            raise GlobalException(message='There are FeatureData related to this entry altready. You need to delete it first', status=HttpStatus.BAD_REQUEST)
        self.featureDataRequestDtoList(dto.featureDataList)

    @ValidatorMethod(requestClass=[SampleRequestDto, str])
    def putRequestDto(self, dto, key):
        self.existsByKey(key)
        self.featureDataRequestDtoList(dto.featureDataList)

    @ValidatorMethod(requestClass=[SampleRequestDto, str, int])
    def patchRequestDto(self, dto, key, value):
        self.existsByKey(key)
        self.featureDataRequestDtoList(dto.featureDataList)
        if not value and not 0 == value :
            raise GlobalException(message='Value cannot be null', status=HttpStatus.BAD_REQUEST)

    @ValidatorMethod(requestClass=str)
    def notExistsByKey(self, key):
        self.validator.common.strNotNull(key, 'key')
        if self.service.sample.existsByKey(key):
            raise GlobalException(message='Sample already exists', status=HttpStatus.BAD_REQUEST)

    @ValidatorMethod(requestClass=str)
    def existsByKey(self, key):
        self.validator.common.strNotNull(key, 'key')
        if not self.service.sample.existsByKey(key):
            raise GlobalException(message='''Sample does not exists''', status=HttpStatus.BAD_REQUEST)

    @ValidatorMethod(requestClass=[[Feature], [FeatureData]])
    def listLengthAreEqualsInSampleMapping(self, featureList, featureDataList):
        if not len(featureList) == len(featureDataList):
            logMessage = f'Error mapping Sample. Invalid list length: {featureList} and {featureDataList}'
            if len(featureList) > len(featureDataList):
                raise GlobalException(logMessage=logMessage)
            elif len(featureList) < len(featureDataList):
                raise GlobalException(
                    message = f'Some features were not found. Make shure to post them before you add it to a sample',
                    logMessage = logMessage,
                    status = HttpStatus.BAD_REQUEST
                )

    @ValidatorMethod(requestClass=[[FeatureDataRequestDto]])
    def featureDataRequestDtoList(self, featureDataList):
        for featureDataPostRequestDto in featureDataList :
            if not featureDataPostRequestDto.featureKey :
                raise GlobalException(message='All featureDataList items must contain featureKey', status=HttpStatus.BAD_REQUEST)

    @ValidatorMethod(requestClass=[[BestFitRequestDto], int])
    def bestFitRequestDtoList(self, bestFitList, amount):
        if amount < DefaultValue.MIN_QUERY_AMMOUNT :
            raise GlobalException(message=f'Amount must be greater or equals to {DefaultValue.MIN_QUERY_AMMOUNT}', status=HttpStatus.BAD_REQUEST)
        if amount > DefaultValue.MAX_QUERY_AMMOUNT :
            raise GlobalException(message=f'Amount limited at {DefaultValue.MAX_QUERY_AMMOUNT}', status=HttpStatus.BAD_REQUEST)
        for bestFit in bestFitList :
            if not bestFit.featureKey :
                raise GlobalException(message='The attribute "featureKey" cannot be null', status=HttpStatus.BAD_REQUEST)
