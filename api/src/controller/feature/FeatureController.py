from python_framework import Controller, ControllerMethod, HttpStatus
from Role import *

from dto.FeatureDto import *

@Controller(url = '/features', tag='Feature', description='Single Feature controller')
class FeatureController:

    @ControllerMethod(url='/<string:key>',
        requestClass=FeatureRequestDto,
        responseClass=FeatureResponseDto,
        apiKeyRequired=[ADMIN, API]
        , logRequest = True
        , logResponse = True
    )
    def post(self, dto, key):
        return self.service.feature.create(dto, key), HttpStatus.CREATED

    @ControllerMethod(url='/<string:key>',
        responseClass=FeatureResponseDto,
        apiKeyRequired=[ADMIN, API]
        # , logRequest = True
        # , logResponse = True
    )
    def get(self, key=None):
        return self.service.feature.queryByKey(key), HttpStatus.OK

    @ControllerMethod(url='/<string:key>',
        requestClass=FeatureRequestDto,
        responseClass=FeatureResponseDto,
        apiKeyRequired=[ADMIN, API]
        # , logRequest = True
        # , logResponse = True
    )
    def put(self, dto, key):
        return self.service.feature.update(dto, key), HttpStatus.ACCEPTED

    @ControllerMethod(url='/<string:key>',
        apiKeyRequired=[ADMIN]
        , logRequest = True
        , logResponse = True
    )
    def delete(self, key):
        return self.service.feature.delete(key), HttpStatus.NO_CONTENT


@Controller(url = '/features/all', tag='Feature', description='Multiple Feature controller')
class FeatureBatchController:

    @ControllerMethod(
        responseClass=[[FeatureResponseDto]],
        apiKeyRequired=[ADMIN]
        # , logRequest = True
        # , logResponse = True
    )
    def get(self):
        return self.service.feature.queryAll(), HttpStatus.OK
