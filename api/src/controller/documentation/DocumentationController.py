from FlaskManager import Controller, ControllerMethod
import HttpStatus


@Controller(url='/swagger-io', tag='Documentation', description='OpenApi documentation')
class DocumentationController:

    @ControllerMethod(responseClass=dict)
    def get(self):
        return self.service.documentation.getSwaggerDocumentation(), HttpStatus.OK
