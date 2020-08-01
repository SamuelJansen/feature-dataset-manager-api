from FlaskManager import Controller, ControllerMethod
from Role import *
import BestFitDto, HttpStatus

@Controller(url = '/best-fit')
class BestFitController:

    @ControllerMethod(url='/<int:amount>', requestClass=[[BestFitDto.BestFitRequestDto]], roleRequired=[USER, ADMIN])
    def post(self, bestFitList, amount=None):
        return self.service.sample.queryBestFitList(bestFitList, amount), HttpStatus.OK
