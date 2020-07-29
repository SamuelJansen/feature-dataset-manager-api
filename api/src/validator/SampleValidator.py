from FlaskHelper import Validator, ValidatorMethod
import SampleDto, Sample, Feature, FeatureData, FeatureDataDto, GlobalException, HttpStatus

@Validator()
class SampleValidator:

    @ValidatorMethod(requestClass=SampleDto.SamplePostRequestDto)
    def postRequestDto(self,dto):
        self.notExistsByKey(dto.key)
        if not len(self.service.featureData.findAllBySampleKey(dto.key)) == 0 :
            raise GlobalException.GlobalException(message='There are FeatureData related to this entry altready. You need to delete it first', status=HttpStatus.BAD_REQUEST)
        self.featureDataPostRequestDtoList(dto.featureDataList)

    @ValidatorMethod(requestClass=[SampleDto.SampleRequestDto, str().__class__])
    def putRequestDto(self, dto, key):
        self.existsByKey(key)
        self.featureDataRequestDtoList(dto.featureDataList)
        if not dto.value and not 0 == dto.value :
            raise GlobalException.GlobalException(message='Value cannot be null', status=HttpStatus.BAD_REQUEST)

    @ValidatorMethod(requestClass=str().__class__)
    def notExistsByKey(self, key):
        if self.service.sample.existsByKey(key) :
            raise GlobalException.GlobalException(message='Sample already exists', status=HttpStatus.BAD_REQUEST)

    @ValidatorMethod(requestClass=str().__class__)
    def existsByKey(self, key):
        if not self.service.sample.existsByKey(key) :
            raise GlobalException.GlobalException(message='''Sample does not exists''', status=HttpStatus.BAD_REQUEST)

    @ValidatorMethod(requestClass=[[Feature.Feature], [FeatureData.FeatureData]])
    def listLengthAreEqualsInSampleMapping(self, featureList, featureDataList) :
        if not len(featureList) == len(featureDataList) :
            logMessage = f'Error mapping Sample. Invalid list length: {featureList} and {featureDataList}'
            if len(featureList) > len(featureDataList) :
                raise GlobalException.GlobalException(logMessage=logMessage)
            elif len(featureList) < len(featureDataList) :
                raise GlobalException.GlobalException(
                    message = f'Some features were not found. Make shure to post them before you add it to a sample',
                    logMessage = logMessage,
                    status = HttpStatus.BAD_REQUEST
                )

    @ValidatorMethod(requestClass=[Sample.Sample])
    def model(self, model) :
        ...

    @ValidatorMethod(requestClass=[[FeatureDataDto.FeatureDataPostRequestDto]])
    def featureDataPostRequestDtoList(self, featureDataList):
        self.validateFeatureDataList(featureDataList)

    @ValidatorMethod(requestClass=[[FeatureDataDto.FeatureDataRequestDto]])
    def featureDataRequestDtoList(self, featureDataList):
        self.validateFeatureDataList(featureDataList)

    def validateFeatureDataList(self, featureDataList):
        for featureDataPostRequestDto in featureDataList :
            if not featureDataPostRequestDto.featureKey :
                raise GlobalException.GlobalException(message='All featureDataList items must contain featureKey')
