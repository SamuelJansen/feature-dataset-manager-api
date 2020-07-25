from FlaskHelper import Service, ServiceMethod
import Skill, SkillPostDto, GlobalException, HttpStatus

@Service()
class SkillService:

    def findAll(self):
        return self.repository.skill.findAll()

    def findByKey(self,key):
        return self.repository.skill.findByKey(key)

    @ServiceMethod(requestClass=[SkillPostDto.SkillPostDto])
    def create(self,requestDto):
        self.validator.skill.validadeSkillRequestDto(requestDto)
        if self.repository.skill.notExistsByKey(requestDto.key) :
            newSkill = self.mapper.skill.mapFromPostDtoToModel(requestDto)
            skill = self.repository.skill.save(newSkill)
            return self.converter.skill.convertFromModelToDto(skill)
        raise GlobalException.GlobalException(message='Skill already exists', status=HttpStatus.BAD_REQUEST)
