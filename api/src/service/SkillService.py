from FlaskHelper import Service
import Skill

@Service()
class SkillService:

    def findAll(self):
        return self.repository.skill.findAll()

    def findByKey(self,key):
        return self.repository.skill.findByKey(key)

    def create(self,skillRequestDto):
        if self.repository.skill.notExistsByKey(skillRequestDto.key) :
            newSkill = self.converter.skill.convertFromDtoToModel(skillRequestDto)
            skill = self.repository.skill.save(newSkill)
            return self.converter.skill.convertFromModelToDto(skill)
        self.abort(400, description='Skill already exists')
