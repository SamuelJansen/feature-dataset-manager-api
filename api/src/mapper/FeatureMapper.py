from python_framework import Mapper, MapperMethod

from Feature import Feature
from dto.FeatureDto import FeatureRequestDto

import DefaultValue

@Mapper()
class FeatureMapper:

    @MapperMethod(requestClass=[FeatureRequestDto, str], responseClass=Feature)
    def fromPostRequestDtoToModel(self, dto, key, model) :
        model.key = key
        model.value = DefaultValue.DEFAULT_VALUE
        model.iterationCount = DefaultValue.DEFAULT_ITERATION_COUNT
        return model
