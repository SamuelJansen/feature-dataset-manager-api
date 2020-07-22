from FlaskHelper import Service

@Service()
class OwnerService:

    def findAll(self) :
        return self.repository.owner.findAll()
