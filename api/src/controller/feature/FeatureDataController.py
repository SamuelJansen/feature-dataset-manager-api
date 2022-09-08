from python_framework import Controller, ControllerMethod, HttpStatus
from Role import *

from dto.FeatureDataDto import *

@Controller(url = '/feature-datas', tag='FeatureData', description='Single FeatureData controller')
class FeatureDataController:

    @ControllerMethod(url='/<string:featureKey>/<string:sampleKey>',
        responseClass=FeatureDataResponseDto,
        apiKeyRequired=[ADMIN, API]
        # , logRequest = True
        # , logResponse = True
    )
    def get(self, featureKey, sampleKey):
        return self.service.featureData.queryByFeatureKeyAndSampleKey(featureKey, sampleKey), HttpStatus.OK

    @ControllerMethod(url='/<string:featureKey>/<string:sampleKey>',
        apiKeyRequired=[ADMIN]
        # , logRequest = True
        # , logResponse = True
    )
    def delete(self, featureKey, sampleKey):
        return self.service.featureData.deleteByFeatureKeyAndSampleKey(featureKey, sampleKey), HttpStatus.NO_CONTENT


@Controller(url = '/feature-datas/all', tag='FeatureData', description='Multiple FeatureData controller')
class FeatureDataBatchController:

    @ControllerMethod(url='/<string:featureKey>',
        responseClass=[[FeatureDataResponseDto]],
        apiKeyRequired=[ADMIN]
        # , logRequest = True
        # , logResponse = True
    )
    def get(self, featureKey):
        return self.service.featureData.queryAllByFeatureKey(featureKey), HttpStatus.OK
