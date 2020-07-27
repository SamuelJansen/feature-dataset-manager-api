from FlaskHelper import Mapper, MapperMethod
import Feature, FeatureDto

DEFAULT_VALUE = 3

@Mapper()
class FeatureMapper:

    @MapperMethod(requestClass=FeatureDto.FeaturePostRequestDto, responseClass=Feature.Feature)
    def fromPostDtoToModel(self, dto, model) :
        model.value = DEFAULT_VALUE
        return model

    @MapperMethod(requestClass=[FeatureDto.FeatureRequestDto, Feature.Feature])
    def fromRequestDtoToModel(self, dto, model) :
        model.label = dto.label
        return model
