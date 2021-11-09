from python_framework import Repository

from SampleData import SampleData

@Repository(model = SampleData)
class SampleDataRepository:

    def findAll(self):
        return self.repository.findAllAndCommit(self.model)
