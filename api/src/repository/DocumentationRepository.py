from python_framework import Repository, OpenApiDocumentationFile

@Repository()
class DocumentationRepository:

    def getSwaggerDocumentation(self):
        import sys
        sys.path.append(self.globals.OS_SEPARATOR + self.globals.api.documentationFolderPath)
        trying = f'C:{self.globals.OS_SEPARATOR}Users{self.globals.OS_SEPARATOR}Samuel Jansen{self.globals.OS_SEPARATOR}AppData{self.globals.OS_SEPARATOR}Roaming{self.globals.OS_SEPARATOR}Python{self.globals.OS_SEPARATOR}dist'
        sys.path.append(trying)
        print(self.globals.OS_SEPARATOR + self.globals.api.documentationFolderPath)
        import site
        print(str(site.getsitepackages()).replace('\\\\',self.globals.OS_SEPARATOR).replace('/',self.globals.OS_SEPARATOR).replace('\\',self.globals.OS_SEPARATOR))


        sys.path.append(f'C:{self.globals.OS_SEPARATOR}Users{self.globals.OS_SEPARATOR}Samuel Jansen{self.globals.OS_SEPARATOR}AppData{self.globals.OS_SEPARATOR}Local{self.globals.OS_SEPARATOR}Programs{self.globals.OS_SEPARATOR}Python{self.globals.OS_SEPARATOR}Python38-32{self.globals.OS_SEPARATOR}dist{self.globals.OS_SEPARATOR}')
        return OpenApiDocumentationFile.loadDocumentation(self.globals.api)
