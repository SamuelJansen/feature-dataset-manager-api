from FlaskHelper import Validator, ValidatorMethod
import FeatureDataDto, GlobalException, HttpStatus

@Validator()
class FeatureDataValidator:

    @ValidatorMethod()
    def postRequestDtoList(self, postRequestDtoList):
        expecteObjectClass = FeatureDataDto.FeatureDataPostRequestDto
        for dto in postRequestDtoList :
            if not FeatureDataDto.FeatureDataPostRequestDto.__name__ == dto.__class__.__name__ :
                GlobalException.validateArgs(self,self.postRequestDtoList,dto,expecteObjectClass)
