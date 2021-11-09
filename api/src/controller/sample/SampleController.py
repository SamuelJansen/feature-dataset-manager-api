from python_framework import Controller, ControllerMethod, HttpStatus
from Role import *

from dto.SampleDto import SampleRequestDto, SampleResponseDto

@Controller(url = '/samples', tag='Sample', description='Single Sample controller')
class SampleController:

    @ControllerMethod(url='/<string:key>',
        requestClass=SampleRequestDto,
        responseClass=SampleResponseDto,
        apiKeyRequired=[ADMIN, API]
        , logRequest = True
        , logResponse = True
    )
    def post(self, dto, key):
        return self.service.sample.create(dto, key), HttpStatus.CREATED

    @ControllerMethod(url='/<string:key>',
        responseClass=SampleResponseDto,
        apiKeyRequired=[ADMIN, API]
        # , logRequest = True
        # , logResponse = True
    )
    def get(self, key):
        return self.service.sample.queryByKey(key), HttpStatus.OK

    @ControllerMethod(url='/<string:key>/<int:value>',
        requestClass=SampleRequestDto,
        responseClass=SampleResponseDto,
        apiKeyRequired=[ADMIN, API]
        # , logRequest = True
        # , logResponse = True
    )
    def patch(self, dto, key, value):
        return self.service.sample.patch(dto, key, value), HttpStatus.ACCEPTED

    @ControllerMethod(url='/<string:key>',
        requestClass=SampleRequestDto,
        responseClass=SampleResponseDto,
        apiKeyRequired=[ADMIN, API]
        # , logRequest = True
        # , logResponse = True
    )
    def put(self, dto, key):
        return self.service.sample.update(dto, key), HttpStatus.ACCEPTED

    @ControllerMethod(url='/<string:key>',
        apiKeyRequired=[ADMIN]
        , logRequest = True
        , logResponse = True
    )
    def delete(self, key):
        return self.service.sample.delete(key), HttpStatus.NO_CONTENT, HttpStatus.NO_CONTENT


@Controller(url = '/samples/batch', tag='Sample', description='Multiple Sample controller')
class SampleBatchController:

    @ControllerMethod(
        responseClass=[[SampleResponseDto]],
        apiKeyRequired=[ADMIN]
        # , logRequest = True
        # , logResponse = True
    )
    def get(self):
        return self.service.sample.queryAll(), HttpStatus.OK
