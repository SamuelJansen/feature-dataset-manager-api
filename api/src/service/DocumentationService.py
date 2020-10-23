from python_framework import Service, ServiceMethod

@Service()
class DocumentationService:

    @ServiceMethod()
    def getSwaggerDocumentation(self):
        return self.repository.documentation.getSwaggerDocumentation()
