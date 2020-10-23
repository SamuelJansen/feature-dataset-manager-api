class BestFitRequestDto :
    def __init__(self,
        featureKey = None
    ):
        self.featureKey = featureKey

class BestFitResponseDto :
    def __init__(self,
        key = None,
        label = None,
        value = None,
        iterationCount = None,
        featureDataList = None
    ):
        self.key = key
        self.label = label
        self.value = value
        self.iterationCount = iterationCount
        self.featureDataList = featureDataList if featureDataList else []
