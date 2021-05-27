from python_framework import Validator, ValidatorMethod, GlobalException, HttpStatus
import FeatureDataDto

@Validator()
class FeatureDataValidator:

    @ValidatorMethod(requestClass=[str, str])
    def existsByFeatureKeyAndSampleKey(self, featureKey, sampleKey):
        self.validator.common.pathVariableNotNull(featureKey, 'featureKey')
        self.validator.common.pathVariableNotNull(sampleKey, 'sampleKey')
        if not self.service.featureData.existsByFeatureKeyAndSampleKey(featureKey, sampleKey) :
            raise GlobalException(message='''FeatureData not found''', status=HttpStatus.NOT_FOUND)
