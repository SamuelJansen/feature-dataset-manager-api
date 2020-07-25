from flask import request
from python_helper import Constant
import HttpStatus
import datetime

DEFAULT_MESSAGE = 'Something bad happened. Please, try again later'
DEFAULT_STATUS = HttpStatus.INTERNAL_SERVER_ERROR
DEFAULT_LOG_MESSAGE = Constant.NOTHING

class GlobalException(Exception):
    def __init__(self,
        message = None,
        status = None,
        logMessage = None
    ):
        self.timeStamp = datetime.datetime.now()
        self.message = message if message else DEFAULT_MESSAGE
        self.status = status if status else DEFAULT_STATUS
        self.url = request.url
        self.logMessage = logMessage if logMessage else DEFAULT_LOG_MESSAGE
        self.logPayload = self.getRequestBody()

    def __str__(self):
        return f'''[{self.timeStamp}] {GlobalException.__name__} thrown. Status: {self.status}, message: {self.message}, url: {self.url}{', logMessage: ' if self.logMessage else Constant.NOTHING}{self.logMessage}'''

    def getRequestBody(self) :
        try :
            requestBody = request.get_json()
        except :
            self.message = 'Not possible to parse the request'
            self.status = HttpStatus.BAD_REQUEST
            try :
                requestBody = request.get_data() ###-
            except :
                requestBody = {}
        return requestBody
