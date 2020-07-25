from SqlAlchemyHelper import *
from ModelAssociation import Model, HTTP_ERROR_LOG

MAX_HTTP_ERROR_LOG_PAYLOAD_SIZE = 16384
MAX_MESSAGE_SIZE = 512
MAX_URL_SIZE = 512

class ErrorLog(Model):
    __tablename__ = HTTP_ERROR_LOG

    id = Column(Integer(), Sequence(f'{__tablename__}{ID}{SEQ}'), primary_key=True)
    timeStamp = Column(DateTime())
    status = Column(Integer())
    message = Column(String(MAX_MESSAGE_SIZE))
    url = Column(String(MAX_URL_SIZE))
    logMessage = Column(String(MAX_MESSAGE_SIZE))
    logPayload = Column(String(MAX_HTTP_ERROR_LOG_PAYLOAD_SIZE))

    def __init__(self,
        id = None,
        timeStamp = None,
        status = None,
        message = None,
        url = None,
        logMessage = None,
        logPayload = None
    ):
        self.timeStamp = timeStamp
        self.status = status
        self.message = str(message)[:MAX_MESSAGE_SIZE-1]
        self.url = str(url)[:MAX_URL_SIZE-1]
        self.logMessage = str(logMessage)[:MAX_MESSAGE_SIZE-1]
        self.logPayload = str(logPayload)[:MAX_HTTP_ERROR_LOG_PAYLOAD_SIZE-1]
        self.id = id

    def override(self,globalException):
        self.timeStamp = globalException.timeStamp
        self.status = globalException.status
        self.message = str(globalException.message)[:MAX_MESSAGE_SIZE-1]
        self.url = str(globalException.url)[:MAX_URL_SIZE-1]
        self.logMessage = str(globalException.logMessage)[:MAX_MESSAGE_SIZE-1]
        self.logPayload = str(globalException.logPayload)[:MAX_HTTP_ERROR_LOG_PAYLOAD_SIZE-1]

    def __repr__(self):
        return f'{HTTP_ERROR_LOG}(status={self.status}, message={self.message}, url={self.url}, id={self.id})'
