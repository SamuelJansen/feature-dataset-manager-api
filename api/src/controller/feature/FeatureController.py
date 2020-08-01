from FlaskHelper import Controller, ControllerMethod
import Role
import FeatureDto
import HttpStatus

@Controller(url = '/features')
class FeatureController:

    @ControllerMethod(url='/<key>', requestClass=FeatureDto.FeatureRequestDto, roleRequired=[Role.USER])
    def post(self, dto, key):
        return self.service.feature.create(dto, key), HttpStatus.CREATED

    @ControllerMethod(url='/<key>', roleRequired=[Role.USER])
    def get(self, key=None):
        return self.service.feature.queryByKey(key), HttpStatus.OK

    @ControllerMethod(url='/<key>', requestClass=FeatureDto.FeatureRequestDto, roleRequired=[Role.USER])
    def put(self, dto, key):
        return self.service.feature.update(dto, key), HttpStatus.ACCEPTED

    @ControllerMethod(url='/<key>', roleRequired=[Role.ADMIN])
    def delete(self, key):
        self.service.feature.delete(key)
        return {}, HttpStatus.NO_CONTENT


@Controller(url = '/features/batch')
class FeatureBatchController:

    @ControllerMethod(roleRequired=[Role.ADMIN])
    def get(self):
        return self.service.feature.queryAll(), HttpStatus.OK
