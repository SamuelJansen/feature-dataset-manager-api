from FlaskHelper import Repository
import OwnerData

@Repository(model = OwnerData.OwnerData)
class OwnerDataRepository:

    def findAll(self) :
        return self.repository.findAllAndCommit(self.model)
