from FlaskHelper import Converter, ConverterMethod
import Skill, SkillDto

@Converter()
class SkillConverter:

    @ConverterMethod(objectClass = Skill.Skill)
    def convertFromDtoToModel(self, dto, model) :
        return model

    @ConverterMethod(objectClass = SkillDto.SkillDto)
    def convertFromModelToDto(self, model, dto) :
        return dto
