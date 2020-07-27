from FlaskHelper import Validator, ValidatorMethod
import FeatureDto, GlobalException

@Validator()
class FeatureValidator:

    @ValidatorMethod(requestClass=FeatureDto.FeaturePostRequestDto)
    def postRequestDto(self,dto):
        self.notExistsByKey(dto.key)

    @ValidatorMethod(requestClass=FeatureDto.FeatureRequestDto)
    def putRequestDto(self,dto):
        self.existsByKey(dto.key)

    @ValidatorMethod()
    def notExistsByKey(self, key):
        if self.service.feature.existsByKey(key) :
            raise GlobalException.GlobalException(message='Feature already exists', status=HttpStatus.BAD_REQUEST)

    @ValidatorMethod()
    def existsByKey(self, key):
        if not self.service.feature.existsByKey(key) :
            raise GlobalException.GlobalException(message='''Feature does not exists''', status=HttpStatus.NOT_FOUND)
