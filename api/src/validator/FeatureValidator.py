from python_helper import Constant
from FlaskHelper import Validator, ValidatorMethod
import FeatureDto, Feature, GlobalException, HttpStatus

@Validator()
class FeatureValidator:

    @ValidatorMethod(requestClass=FeatureDto.FeaturePostRequestDto)
    def postRequestDto(self,dto):
        self.notExistsByKey(dto.key)

    @ValidatorMethod(requestClass=[FeatureDto.FeatureRequestDto, str().__class__])
    def putRequestDto(self, dto, key):
        self.existsByKey(key)

    @ValidatorMethod(requestClass=str().__class__)
    def notExistsByKey(self, key):
        if self.service.feature.existsByKey(key) :
            raise GlobalException.GlobalException(message=f'Feature already exists. Key : {Constant.SINGLE_QUOTE}{key}{Constant.SINGLE_QUOTE}', status=HttpStatus.BAD_REQUEST)

    @ValidatorMethod(requestClass=str().__class__)
    def existsByKey(self, key):
        if not self.service.feature.existsByKey(key) :
            raise GlobalException.GlobalException(message=f'''Feature does not exists. Key : {Constant.SINGLE_QUOTE}{key}{Constant.SINGLE_QUOTE}''', status=HttpStatus.NOT_FOUND)

    @ValidatorMethod(requestClass=[[Feature.Feature], [str().__class__]])
    def featureListByfeatureKeyList(self, featureList, featureKeyList) :
        for key in featureKeyList :
            notFountYet = True
            for feature in featureList :
                if feature.key in featureKeyList :
                    notFountYet = False
                    break
            if notFountYet :
                raise GlobalException.GlobalException(message=f'''Feature does not exists. Key : {Constant.SINGLE_QUOTE}{key}{Constant.SINGLE_QUOTE}''', status=HttpStatus.BAD_REQUEST)
