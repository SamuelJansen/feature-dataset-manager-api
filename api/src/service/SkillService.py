from FlaskHelper import Service, ServiceMethod
import Skill, SkillDto, GlobalException, HttpStatus

@Service()
class SkillService:

    def findAll(self):
        return self.repository.skill.findAll()

    def findByKey(self,key):
        return self.repository.skill.findByKey(key)

    @ServiceMethod(requestClass=[SkillDto.SkillPostRequestDto])
    def create(self,requestDto):
        self.validator.skill.validadePostRequestDto(requestDto)
        if self.repository.skill.notExistsByKey(requestDto.key) :
            newSkill = self.mapper.skill.mapFromPostDtoToModel(requestDto)
            skill = self.repository.skill.save(newSkill)
            return self.converter.skill.convertFromModelToResponseDto(skill)
        raise GlobalException.GlobalException(message='Skill already exists', status=HttpStatus.BAD_REQUEST)

    @ServiceMethod(requestClass=SkillDto.SkillRequestDto)
    def update(self,requestDto,key):
        self.validator.skill.validadeRequestDto(requestDto)
        if self.repository.skill.existsByKey(key) :
            skill = self.repository.skill.findByKey(key)
            skill = self.mapper.skill.mapFromRequestDtoToModel(requestDto,skill)
            skill = self.repository.skill.save(skill)
            return self.converter.skill.convertFromModelToResponseDto(skill)
        raise GlobalException.GlobalException(message='''Skill doesn't exists''', status=HttpStatus.BAD_REQUEST)

    @ServiceMethod()
    def delete(self,key):
        if self.repository.skill.notExistsByKey(key) :
            raise GlobalException.GlobalException(message='''Skill doesn't exists''', status=HttpStatus.BAD_REQUEST)
        self.repository.skill.deleteByKey(key)
