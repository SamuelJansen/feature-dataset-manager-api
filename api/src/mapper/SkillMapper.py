from FlaskHelper import Mapper, MapperMethod
import Skill, SkillDto

DEFAULT_VALUE = 3

@Mapper()
class SkillMapper:

    @MapperMethod(requestClass=SkillDto.SkillPostRequestDto, responseClass=Skill.Skill)
    def mapFromPostDtoToModel(self, dto, model) :
        model.value = DEFAULT_VALUE
        return model

    @MapperMethod(requestClass=[SkillDto.SkillRequestDto, Skill.Skill])
    def mapFromRequestDtoToModel(self, dto, model) :
        model.label = dto.label
        return model
