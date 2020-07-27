from FlaskHelper import Service, ServiceMethod
import FeatureData

@Service()
class FeatureDataService:

    @ServiceMethod()
    def findAllBySampleKey(self, sampleKey) :
        return self.repository.featureData.findAllBySampleKey(sampleKey)
