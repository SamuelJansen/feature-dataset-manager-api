from python_framework import Controller, ControllerMethod, HttpStatus
from Role import *

from dto.FeatureDto import *

@Controller(url = '/features', tag='Feature', description='Single Feature controller')
class FeatureController:

    @ControllerMethod(url='/<string:key>',
        requestClass=FeatureRequestDto,
        responseClass=FeatureResponseDto,
        roleRequired=[USER, ADMIN, API])
    def post(self, dto, key):
        return self.service.feature.create(dto, key), HttpStatus.CREATED

    @ControllerMethod(url='/<string:key>',
        responseClass=FeatureResponseDto,
        roleRequired=[USER, ADMIN, API])
    def get(self, key=None):
        return self.service.feature.queryByKey(key), HttpStatus.OK

    @ControllerMethod(url='/<string:key>',
        requestClass=FeatureRequestDto,
        responseClass=FeatureResponseDto,
        roleRequired=[USER, ADMIN, API])
    def put(self, dto, key):
        return self.service.feature.update(dto, key), HttpStatus.ACCEPTED

    @ControllerMethod(url='/<string:key>',
        roleRequired=[ADMIN, API])
    def delete(self, key):
        self.service.feature.delete(key)
        return {}, HttpStatus.NO_CONTENT


@Controller(url = '/features/batch', tag='Feature', description='Multiple Feature controller')
class FeatureBatchController:

    @ControllerMethod(
        responseClass=[[FeatureResponseDto]],
        roleRequired=[ADMIN, API])
    def get(self):
        return self.service.feature.queryAll(), HttpStatus.OK
