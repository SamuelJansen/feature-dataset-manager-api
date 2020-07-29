class SampleDto :
    def __init__(self,
            id = None,
            key = None,
            label = None,
            value = None,
            iterationCount = None,
            featureDataList = None
        ):
        self.id = id
        self.key = key
        self.label = label
        self.value = value
        self.iterationCount = iterationCount
        self.featureDataList = featureDataList if featureDataList else []

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
