from python_framework import Controller, ControllerMethod, HttpStatus
from Role import *
import SampleDto

@Controller(url = '/samples', tag='Sample', description='Single Sample controller')
class SampleController:

    @ControllerMethod(url='/<string:key>',
        requestClass=SampleDto.SampleRequestDto,
        responseClass=SampleDto.SampleResponseDto,
        roleRequired=[USER, ADMIN])
    def post(self, dto, key):
        return self.service.sample.create(dto, key), HttpStatus.CREATED

    @ControllerMethod(url='/<string:key>',
        responseClass=SampleDto.SampleResponseDto,
        roleRequired=[USER, ADMIN])
    def get(self, key):
        return self.service.sample.queryByKey(key), HttpStatus.OK

    @ControllerMethod(url='/<string:key>/<int:value>',
        requestClass=SampleDto.SampleRequestDto,
        responseClass=SampleDto.SampleResponseDto,
        roleRequired=[USER, ADMIN])
    def patch(self, dto, key, value):
        return self.service.sample.patch(dto, key, value), HttpStatus.ACCEPTED

    @ControllerMethod(url='/<string:key>',
        requestClass=SampleDto.SampleRequestDto,
        responseClass=SampleDto.SampleResponseDto,
        roleRequired=[USER, ADMIN])
    def put(self, dto, key):
        return self.service.sample.update(dto, key), HttpStatus.ACCEPTED

    @ControllerMethod(url='/<string:key>',
        roleRequired=[ADMIN])
    def delete(self, key):
        self.service.sample.delete(key), HttpStatus.NO_CONTENT
        return {}, HttpStatus.NO_CONTENT


@Controller(url = '/samples/batch', tag='Sample', description='Multiple Sample controller')
class SampleBatchController:

    @ControllerMethod(
        responseClass=[[SampleDto.SampleResponseDto]],
        roleRequired=[ADMIN])
    def get(self):
        return self.service.sample.queryAll(), HttpStatus.OK
