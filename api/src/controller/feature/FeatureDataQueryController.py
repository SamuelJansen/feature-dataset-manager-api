from python_framework import Controller, ControllerMethod, HttpStatus
from Role import *

from dto import FeatureDataDto

@Controller(url = '/feature-datas', tag='FeatureData', description='Multiple FeatureData controller')
class FeatureDataQueryBatchController:

    @ControllerMethod(url='/query/all',
        responseClass=[[FeatureDataDto.FeatureDataResponseDto]],
        requestParamClass = [FeatureDataDto.FeatureDataQueryRequestParamDto],
        apiKeyRequired=[ADMIN]
        # , logRequest = True
        # , logResponse = True
    )
    def get(self, params=None):
        return self.service.featureData.queryAll(params), HttpStatus.OK
