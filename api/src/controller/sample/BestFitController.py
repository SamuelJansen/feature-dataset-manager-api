from python_framework import Controller, ControllerMethod, HttpStatus
from Role import *

from dto.BestFitDto import *

@Controller(url = '/best-fit', tag='BestFit', description='You can get the best Sample fit given a feature set')
class BestFitController:

    @ControllerMethod(url='/<int:amount>',
        requestClass=[[BestFitRequestDto]],
        responseClass=[[BestFitResponseDto]],
        apiKeyRequired=[ADMIN, API]
        # , logRequest = True
        # , logResponse = True
    )
    def post(self, bestFitList, amount=None):
        return self.service.sample.queryBestFitList(bestFitList, amount), HttpStatus.OK
