from python_framework import Controller, ControllerMethod, HttpStatus
from Role import *

from dto.SampleDto import SampleRequestDto, SampleResponseDto

@Controller(url = '/samples', tag='Sample', description='Single Sample controller')
class SampleController:

    @ControllerMethod(url='/<string:key>',
        requestClass=SampleRequestDto,
        responseClass=SampleResponseDto,
        roleRequired=[USER, ADMIN, API])
    def post(self, dto, key):
        return self.service.sample.create(dto, key), HttpStatus.CREATED

    @ControllerMethod(url='/<string:key>',
        responseClass=SampleResponseDto,
        roleRequired=[USER, ADMIN, API])
    def get(self, key):
        return self.service.sample.queryByKey(key), HttpStatus.OK

    @ControllerMethod(url='/<string:key>/<int:value>',
        requestClass=SampleRequestDto,
        responseClass=SampleResponseDto,
        roleRequired=[USER, ADMIN, API])
    def patch(self, dto, key, value):
        return self.service.sample.patch(dto, key, value), HttpStatus.ACCEPTED

    @ControllerMethod(url='/<string:key>',
        requestClass=SampleRequestDto,
        responseClass=SampleResponseDto,
        roleRequired=[USER, ADMIN, API])
    def put(self, dto, key):
        return self.service.sample.update(dto, key), HttpStatus.ACCEPTED

    @ControllerMethod(url='/<string:key>',
        roleRequired=[ADMIN, API])
    def delete(self, key):
        return self.service.sample.delete(key), HttpStatus.NO_CONTENT, HttpStatus.NO_CONTENT


@Controller(url = '/samples/batch', tag='Sample', description='Multiple Sample controller')
class SampleBatchController:

    @ControllerMethod(
        responseClass=[[SampleResponseDto]],
        roleRequired=[ADMIN, API])
    def get(self):
        return self.service.sample.queryAll(), HttpStatus.OK
