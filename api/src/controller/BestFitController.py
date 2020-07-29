from FlaskHelper import Controller, ControllerMethod
import HttpStatus

@Controller(url = '/best-fit')
class BestFitController:

    @ControllerMethod(url='/')
    def get(self):
        return self.service.feature.queryBestFit(), HttpStatus.OK


@Controller(url = '/best-fit')
class BestFitBatchController:

    @ControllerMethod(url='/<ammount>')
    def get(self, ammount=None):
        return self.service.feature.queryBestFitByAmmount(ammount), HttpStatus.OK
