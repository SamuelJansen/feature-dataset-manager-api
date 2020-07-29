from FlaskHelper import Controller, ControllerMethod
import FeatureDataDto, HttpStatus

@Controller(url = '/feature-datas')
class FeatureDataController:

    @ControllerMethod(url='/<featureKey>/<sampleKey>')
    def get(self, featureKey, sampleKey):
        return self.service.featureData.queryByFeatureKeyAndSampleKey(featureKey, sampleKey), HttpStatus.OK

    @ControllerMethod(url='/<featureKey>/<sampleKey>')
    def delete(self, featureKey, sampleKey):
        return self.service.featureData.deleteByFeatureKeyAndSampleKey(featureKey, sampleKey), HttpStatus.NO_CONTENT


@Controller(url = '/feature-datas/batch')
class FeatureDataBatchController:

    @ControllerMethod(url='/<featureKey>')
    def get(self, featureKey):
        print(featureKey)
        return self.service.featureData.queryAllByFeatureKey(featureKey), HttpStatus.OK
