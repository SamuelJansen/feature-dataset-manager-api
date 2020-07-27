from FlaskHelper import Validator, ValidatorMethod
import SampleDto, GlobalException, HttpStatus

@Validator()
class SampleValidator:

    @ValidatorMethod(requestClass=SampleDto.SamplePostRequestDto)
    def postRequestDto(self,dto):
        self.notExistsByKey(dto.key)
        if not len(self.service.featureData.findAllBySampleKey(dto.key)) == 0 :
            raise GlobalException.GlobalException(message='There are FeatureData related to this entry altready. You need to delete it first', status=HttpStatus.BAD_REQUEST)
        self.featureDataList(dto.featureDataList)

    @ValidatorMethod(requestClass=[SampleDto.SampleRequestDto, str().__class__])
    def putRequestDto(self, dto, key):
        self.existsByKey(key)
        self.featureDataList(dto.featureDataList)

    @ValidatorMethod()
    def notExistsByKey(self, key):
        if self.service.sample.existsByKey(key) :
            raise GlobalException.GlobalException(message='Sample already exists', status=HttpStatus.BAD_REQUEST)

    @ValidatorMethod()
    def existsByKey(self, key):
        if not self.service.sample.existsByKey(key) :
            raise GlobalException.GlobalException(message='''Sample does not exists''', status=HttpStatus.BAD_REQUEST)

    @ValidatorMethod()
    def featureDataList(self, featureDataList):
        for featureDataPostRequestDto in featureDataList :
            if not featureDataPostRequestDto.featureKey :
                raise GlobalException.GlobalException(message='All featureDataList items must contain featureKey')

    @ValidatorMethod(requestClass=[list().__class__, list().__class__])
    def listLengthAreEqualsInSampleMapping(self, firsList, sencondList) :
        if not len(firsList) == len(sencondList) :
            raise GlobalException(logMessage=f'Error mapping Sample. invalid list length: {firsList} and {sencondList}')
