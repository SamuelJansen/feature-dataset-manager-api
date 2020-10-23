from python_framework import Controller, ControllerMethod, HttpStatus
from Role import *
import BestFitDto

@Controller(url = '/best-fit', tag='BestFit', description='You can get the best Sample fit given a feature set')
class BestFitController:

    @ControllerMethod(url='/<int:amount>',
        requestClass=[[BestFitDto.BestFitRequestDto]],
        responseClass=[[BestFitDto.BestFitResponseDto]],
        roleRequired=[USER, ADMIN])
    def post(self, bestFitList, amount=None):
        return self.service.sample.queryBestFitList(bestFitList, amount), HttpStatus.OK
