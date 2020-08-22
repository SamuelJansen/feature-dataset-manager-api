from FlaskManager import Controller, ControllerMethod
import OpenApiManager
import HttpStatus


@Controller(url='/swagger-io', tag='Documentation', description='OpenApi documentation')
class DocumentationController:

    @ControllerMethod(url='/')
    def get(self):
        return OpenApiManager.loadDocumentation(self.api.globals), HttpStatus.OK
