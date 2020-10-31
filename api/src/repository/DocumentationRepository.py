from python_framework import Repository, OpenApiDocumentationFile

@Repository()
class DocumentationRepository:

    def getSwaggerDocumentation(self):
        import sys
        sys.path.append(self.globals.api.documentationFolderPath)
        return OpenApiDocumentationFile.loadDocumentation(self.globals.api)
