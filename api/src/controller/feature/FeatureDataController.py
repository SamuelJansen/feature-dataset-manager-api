from FlaskManager import Controller, ControllerMethod
from Role import *
import FeatureDataDto, HttpStatus

@Controller(url = '/feature-datas')
class FeatureDataController:

    @ControllerMethod(url='/<string:featureKey>/<string:sampleKey>', roleRequired=[USER, ADMIN])
    def get(self, featureKey, sampleKey):
        return self.service.featureData.queryByFeatureKeyAndSampleKey(featureKey, sampleKey), HttpStatus.OK

    @ControllerMethod(url='/<string:featureKey>/<string:sampleKey>', roleRequired=[USER, ADMIN])
    def delete(self, featureKey, sampleKey):
        self.service.featureData.deleteByFeatureKeyAndSampleKey(featureKey, sampleKey), HttpStatus.NO_CONTENT
        return {}, HttpStatus.NO_CONTENT


@Controller(url = '/feature-datas/batch')
class FeatureDataBatchController:

    @ControllerMethod(url='/<string:featureKey>', roleRequired=[ADMIN])
    def get(self, featureKey):
        return self.service.featureData.queryAllByFeatureKey(featureKey), HttpStatus.OK
