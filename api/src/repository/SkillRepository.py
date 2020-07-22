from FlaskHelper import Repository
import Skill

@Repository(model = Skill.Skill)
class SkillRepository:

    def findAll(self) :
        return self.repository.findAllAndCommit(self.model)

    def existsByKey(self,key) :
        return self.repository.existsByKeyAndCommit(key,self.model)

    def findByKey(self,key) :
        if self.existsByKey(key) :
            return self.repository.findByKeyAndCommit(key,self.model)
        return []

    def notExistsByKey(self,key) :
        return not self.existsByKey(key)

    def save(self,model) :
        return self.repository.saveAndCommit(model)
