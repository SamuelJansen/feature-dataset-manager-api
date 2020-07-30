class FeatureDataResponseDto:
    def __init__(self,
        value = None,
        iterationCount = None,
        featureKey = None,
        sampleKey = None
    ):
        self.value = value
        self.iterationCount = iterationCount
        self.featureKey = featureKey
        self.sampleKey = sampleKey

class FeatureDataRequestDto:
    def __init__(self,
        featureKey = None,
        sampleKey = None
    ):
        self.featureKey = featureKey
        self.sampleKey = sampleKey

class BestFitDataRequestDto :
    def __init__(self,
        featureKey = None,
        featureValue = None,
        sampleKey = None,
        sampleValue = None
    ):
        self.featureKey = featureKey
        self.sampleKey = sampleKey
        self.featureValue = featureValue
        self.sampleValue = sampleValue
