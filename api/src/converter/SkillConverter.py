from FlaskHelper import Converter, ConverterMethod
import Skill, SkillDto

@Converter()
class SkillConverter:

    @ConverterMethod(responseClass=Skill.Skill)
    def convertFromDtoToModel(self, dto, model) :
        return model

    @ConverterMethod(responseClass=SkillDto.SkillResponseDto)
    def convertFromModelToResponseDto(self, model, dto) :
        return dto
