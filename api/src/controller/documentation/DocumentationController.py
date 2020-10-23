from python_framework import Controller, ControllerMethod, HttpStatus

@Controller(url='/swagger-io', tag='Documentation', description='OpenApi documentation')
class DocumentationController:

    @ControllerMethod(responseClass=dict)
    def get(self):
        return self.service.documentation.getSwaggerDocumentation(), HttpStatus.OK
