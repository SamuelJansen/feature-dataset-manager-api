from FlaskManager import Controller, ControllerMethod
from Role import *
import FeatureDataDto, HttpStatus

@Controller(url = '/feature-datas', tag='FeatureData', description='Single FeatureData controller')
class FeatureDataController:

    @ControllerMethod(url='/<string:featureKey>/<string:sampleKey>',
        responseClass=FeatureDataDto.FeatureDataResponseDto,
        roleRequired=[USER, ADMIN])
    def get(self, featureKey, sampleKey):
        return self.service.featureData.queryByFeatureKeyAndSampleKey(featureKey, sampleKey), HttpStatus.OK

    @ControllerMethod(url='/<string:featureKey>/<string:sampleKey>',
        roleRequired=[USER, ADMIN])
    def delete(self, featureKey, sampleKey):
        self.service.featureData.deleteByFeatureKeyAndSampleKey(featureKey, sampleKey), HttpStatus.NO_CONTENT
        return {}, HttpStatus.NO_CONTENT


@Controller(url = '/feature-datas/batch', tag='FeatureData', description='Multiple FeatureData controller')
class FeatureDataBatchController:

    @ControllerMethod(url='/<string:featureKey>',
        responseClass=[[FeatureDataDto.FeatureDataResponseDto]],
        roleRequired=[ADMIN])
    def get(self, featureKey):
        return self.service.featureData.queryAllByFeatureKey(featureKey), HttpStatus.OK
