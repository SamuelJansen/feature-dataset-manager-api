from FlaskHelper import Mapper, MapperMethod
import Skill, SkillPostDto

DEFAULT_VALUE = 3

@Mapper()
class SkillMapper:

    @MapperMethod(requestClass=SkillPostDto.SkillPostDto, responseClass=Skill.Skill)
    def mapFromPostDtoToModel(self, dto, model) :
        model.value = DEFAULT_VALUE
        return model
