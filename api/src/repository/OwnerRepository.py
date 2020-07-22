from FlaskHelper import Repository
import Owner

@Repository(model = Owner.Owner)
class OwnerRepository:

    def findAll(self) :
        return self.repository.findAllAndCommit(self.model)
