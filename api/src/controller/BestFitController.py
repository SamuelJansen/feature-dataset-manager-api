from FlaskHelper import Controller, ControllerMethod
import BestFitDto, HttpStatus

@Controller(url = '/best-fit')
class BestFitController:

    @ControllerMethod(url='/<amount>', requestClass=[[BestFitDto.BestFitRequestDto]])
    def post(self, bestFitList, amount=None):
        return self.service.sample.queryBestFit(bestFitList, int(amount)), HttpStatus.OK
