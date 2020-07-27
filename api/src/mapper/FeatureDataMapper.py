from FlaskHelper import Mapper, MapperMethod
import FeatureData

DEFAULT_VALUE = 3

@Mapper()
class FeatureDataMapper:

    def buildFeatureData(self,value=None) :
        value = value if value else DEFAULT_VALUE
        return
