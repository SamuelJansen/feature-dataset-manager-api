from python_framework import Repository
import User

@Repository(model = User.User)
class UserRepository:

    def findAll(self) :
        return self.repository.findAllAndCommit(self.model)

    def existsByKey(self,key) :
        return self.repository.existsByKeyAndCommit(key, self.model)

    def findByKey(self,key) :
        if self.existsByKey(key) :
            return self.repository.findByKeyAndCommit(key, self.model)

    def notExistsByKey(self,key) :
        return not self.existsByKey(key)

    def save(self,model) :
        return self.repository.saveAndCommit(model)

    def deleteByKey(self,key):
        self.repository.deleteByKeyAndCommit(key, self.model)
