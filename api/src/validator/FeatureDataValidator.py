from python_helper import ObjectHelper
from python_framework import Validator, ValidatorMethod, GlobalException, HttpStatus

from FeatureData import FeatureData

@Validator()
class FeatureDataValidator:

    @ValidatorMethod(requestClass=[str, str])
    def existsByFeatureKeyAndSampleKey(self, featureKey, sampleKey):
        self.validator.common.pathVariableNotNull(featureKey, 'featureKey')
        self.validator.common.pathVariableNotNull(sampleKey, 'sampleKey')
        if not self.service.featureData.existsByFeatureKeyAndSampleKey(featureKey, sampleKey):
            raise GlobalException(message='''FeatureData not found''', status=HttpStatus.NOT_FOUND)

    @ValidatorMethod(requestClass=[FeatureData])
    def validateModelNotNone(self, featureData):
        if ObjectHelper.isNone(featureData):
            raise GlobalException(logMessage='Feature data cannot be None', status=HttpStatus.INTERNAL_SERVER_ERROR)
