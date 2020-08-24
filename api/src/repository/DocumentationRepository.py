from FlaskManager import Repository
import OpenApiDocumentationFile

@Repository()
class DocumentationRepository:

    def getSwaggerDocumentation(self):
        return OpenApiDocumentationFile.loadDocumentation(self.globals)
