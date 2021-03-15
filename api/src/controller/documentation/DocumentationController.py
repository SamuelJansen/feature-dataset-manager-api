from python_helper import EnvironmentHelper
from python_framework import Controller, ControllerMethod, HttpStatus

@Controller(url='/swagger-io', tag='Documentation', description='OpenApi documentation')
class DocumentationController:

    @ControllerMethod(responseClass=dict)
    def get(self):
        return self.service.documentation.getSwaggerDocumentation(), HttpStatus.OK

@Controller(url='/swagger-io/api', tag='Documentation', description='Api Tree')
class DocumentationBatchController:

    @ControllerMethod(url='tree', responseClass=dict)
    def get(self):
        return self.service.documentation.getApiTree(), HttpStatus.OK


    @ControllerMethod(url='config', responseClass=dict)
    def patch(self):
        return self.service.documentation.getGlobalsConfig(), HttpStatus.OK

    @ControllerMethod(responseClass=dict)
    def post(self):
        return {
            'activeEnvironment': EnvironmentHelper.getAcvtiveEnvironment()
        }, HttpStatus.OK
