from python_framework import Controller, ControllerMethod, HttpStatus
from Role import *

from dto.FeatureDataDto import *

@Controller(url = '/feature-datas', tag='FeatureData', description='Single FeatureData controller')
class FeatureDataController:

    @ControllerMethod(url='/<string:featureKey>/<string:sampleKey>',
        responseClass=FeatureDataResponseDto,
        roleRequired=[USER, ADMIN, API])
    def get(self, featureKey, sampleKey):
        return self.service.featureData.queryByFeatureKeyAndSampleKey(featureKey, sampleKey), HttpStatus.OK

    @ControllerMethod(url='/<string:featureKey>/<string:sampleKey>',
        roleRequired=[USER, ADMIN, API])
    def delete(self, featureKey, sampleKey):
        self.service.featureData.deleteByFeatureKeyAndSampleKey(featureKey, sampleKey), HttpStatus.NO_CONTENT
        return {}, HttpStatus.NO_CONTENT


@Controller(url = '/feature-datas/batch', tag='FeatureData', description='Multiple FeatureData controller')
class FeatureDataBatchController:

    @ControllerMethod(url='/<string:featureKey>',
        responseClass=[[FeatureDataResponseDto]],
        roleRequired=[ADMIN, API])
    def get(self, featureKey):
        return self.service.featureData.queryAllByFeatureKey(featureKey), HttpStatus.OK
