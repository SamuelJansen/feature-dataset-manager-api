from FlaskManager import Mapper, MapperMethod
import Feature, FeatureDto, DefaultValue

@Mapper()
class FeatureMapper:

    @MapperMethod(requestClass=[FeatureDto.FeatureRequestDto, str], responseClass=Feature.Feature)
    def fromPostRequestDtoToModel(self, dto, key, model) :
        model.key = key
        model.value = DefaultValue.DEFAULT_VALUE
        model.iterationCount = DefaultValue.DEFAULT_ITERATION_COUNT
        return model

    @MapperMethod(requestClass=[FeatureDto.FeatureRequestDto, Feature.Feature])
    def fromRequestDtoToModel(self, dto, model) :
        model.label = dto.label
        return model
