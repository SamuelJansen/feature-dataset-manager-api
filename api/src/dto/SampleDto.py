class SampleRequestDto :
    def __init__(self,
        label = None,
        featureDataList = None
    ):
        self.label = label
        self.featureDataList = featureDataList if featureDataList else []

class SampleResponseDto :
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
