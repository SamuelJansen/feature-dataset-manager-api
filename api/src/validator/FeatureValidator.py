from python_helper import Constant
from FlaskHelper import Validator, ValidatorMethod
import FeatureDto, Feature, GlobalException, HttpStatus

@Validator()
class FeatureValidator:

    @ValidatorMethod(requestClass=[FeatureDto.FeatureRequestDto, str])
    def postRequestDto(self, dto, key):
        self.notExistsByKey(key)

    @ValidatorMethod(requestClass=[FeatureDto.FeatureRequestDto, str])
    def putRequestDto(self, dto, key):
        self.existsByKey(key)

    @ValidatorMethod(requestClass=str)
    def notExistsByKey(self, key):
        self.validator.common.strNotNull(key, 'key')
        if self.service.feature.existsByKey(key) :
            raise GlobalException.GlobalException(message=f'Feature already exists. Key : {Constant.SINGLE_QUOTE}{key}{Constant.SINGLE_QUOTE}', status=HttpStatus.BAD_REQUEST)

    @ValidatorMethod(requestClass=str)
    def existsByKey(self, key):
        self.validator.common.strNotNull(key, 'key')
        if not self.service.feature.existsByKey(key) :
            raise GlobalException.GlobalException(message=f'''Feature does not exists. Key : {Constant.SINGLE_QUOTE}{key}{Constant.SINGLE_QUOTE}''', status=HttpStatus.NOT_FOUND)

    @ValidatorMethod(requestClass=[[Feature.Feature], [str]])
    def featureListByfeatureKeyList(self, featureList, featureKeyList) :
        for key in featureKeyList :
            notFountYet = True
            for feature in featureList :
                if feature.key in featureKeyList :
                    notFountYet = False
                    break
            if notFountYet :
                raise GlobalException.GlobalException(message=f'''Feature does not exists. Key : {Constant.SINGLE_QUOTE}{key}{Constant.SINGLE_QUOTE}''', status=HttpStatus.BAD_REQUEST)
