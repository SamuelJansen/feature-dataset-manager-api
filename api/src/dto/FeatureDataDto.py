class FeatureDataDto:
    def __init__(self,
        id = None,
        hash = None,
        value = None,
        iterationCount = None,
        feature = None,
        sample = None,
        featureId = None,
        sampleId = None
    ):
        self.id = id
        self.hash = hash
        self.value = value
        self.iterationCount = iterationCount
        self.feature = feature
        self.sample = sample
        self.featureId = featureId
        self.sampleId = sampleId

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
