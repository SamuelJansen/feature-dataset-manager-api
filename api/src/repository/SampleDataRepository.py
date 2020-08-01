from FlaskManager import Repository
import SampleData

@Repository(model = SampleData.SampleData)
class SampleDataRepository:

    def findAll(self) :
        return self.repository.findAllAndCommit(self.model)
