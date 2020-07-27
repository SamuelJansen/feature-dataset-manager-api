from FlaskHelper import Controller, ControllerMethod
import SampleDto, HttpStatus

@Controller(url = '/samples')
class SampleController:

    @ControllerMethod(url='/', requestClass=SampleDto.SamplePostRequestDto)
    def post(self,dto):
        return self.service.sample.create(dto), HttpStatus.CREATED

    @ControllerMethod(url='/<key>')
    def get(self, key=None):
        return self.service.sample.queryByKey(key), HttpStatus.OK

    @ControllerMethod(url='/<key>', requestClass=SampleDto.SampleRequestDto)
    def put(self,dto,key):
        return self.service.sample.update(dto, key), HttpStatus.ACCEPTED

    @ControllerMethod(url='/<key>')
    def delete(self,key):
        return self.service.sample.delete(key), HttpStatus.NO_CONTENT


@Controller(url = '/samples/batch')
class SampleBatchController:

    @ControllerMethod()
    def get(self):
        return self.service.sample.queryAll(), HttpStatus.OK
