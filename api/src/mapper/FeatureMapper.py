from FlaskHelper import Mapper, MapperMethod
import Feature, FeatureDto, DefaultValues

@Mapper()
class FeatureMapper:

    @MapperMethod(requestClass=FeatureDto.FeatureRequestDto, responseClass=Feature.Feature)
    def fromPostRequestDtoToModel(self, dto, model) :
        model.value = DefaultValues.DEFAULT_VALUE
        model.iterationCount = DefaultValues.DEFAULT_ITERATION_COUNT
        return model

    @MapperMethod(requestClass=[FeatureDto.FeatureRequestDto, Feature.Feature])
    def fromRequestDtoToModel(self, dto, model) :
        model.label = dto.label
        return model
