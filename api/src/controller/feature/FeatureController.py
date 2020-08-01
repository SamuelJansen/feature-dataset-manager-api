from FlaskManager import Controller, ControllerMethod
from Role import *
import FeatureDto
import HttpStatus

@Controller(url = '/features')
class FeatureController:

    @ControllerMethod(url='/<string:key>', requestClass=FeatureDto.FeatureRequestDto, roleRequired=[USER, ADMIN])
    def post(self, dto, key):
        return self.service.feature.create(dto, key), HttpStatus.CREATED

    @ControllerMethod(url='/<string:key>', roleRequired=[USER, ADMIN])
    def get(self, key=None):
        return self.service.feature.queryByKey(key), HttpStatus.OK

    @ControllerMethod(url='/<string:key>', requestClass=FeatureDto.FeatureRequestDto, roleRequired=[USER, ADMIN])
    def put(self, dto, key):
        return self.service.feature.update(dto, key), HttpStatus.ACCEPTED

    @ControllerMethod(url='/<string:key>', roleRequired=[ADMIN])
    def delete(self, key):
        self.service.feature.delete(key)
        return {}, HttpStatus.NO_CONTENT


@Controller(url = '/features/batch')
class FeatureBatchController:

    @ControllerMethod(roleRequired=[ADMIN])
    def get(self):
        return self.service.feature.queryAll(), HttpStatus.OK
