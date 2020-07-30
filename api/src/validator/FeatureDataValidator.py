from FlaskHelper import Validator, ValidatorMethod
import FeatureDataDto, GlobalException, HttpStatus

@Validator()
class FeatureDataValidator:

    @ValidatorMethod(requestClass=[str, str])
    def existsByFeatureKeyAndSampleKey(self, featureKey, sampleKey):
        self.featureKeyAndSampleKeyNotNull(featureKey, sampleKey)
        if not self.service.featureData.existsByFeatureKeyAndSampleKey(featureKey, sampleKey) :
            raise GlobalException.GlobalException(message='''FeatureData not found''', status=HttpStatus.NOT_FOUND)

    @ValidatorMethod(requestClass=[str, str])
    def featureKeyAndSampleKeyNotNull(self, featureKey, sampleKey):
        self.featureKeyNotNull(featureKey)
        self.sampleKeyNotNull(sampleKey)

    @ValidatorMethod(requestClass=str)
    def featureKeyNotNull(self, featureKey):
        if not featureKey :
            raise GlobalException.GlobalException(message='''The path variable 'featureKey' cannot be null''', status=HttpStatus.BAD_REQUEST)

    @ValidatorMethod(requestClass=str)
    def sampleKeyNotNull(self, sampleKey):
        if not sampleKey :
            raise GlobalException.GlobalException(message='''The path variable 'sampleKey' cannot be null''', status=HttpStatus.BAD_REQUEST)
